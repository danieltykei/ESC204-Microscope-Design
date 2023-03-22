import time
from microcontroller import cpu
import board
import busio
import pwmio
import digitalio
import asyncio
from digitalio import DigitalInOut
from analogio import AnalogIn
from adafruit_motor import stepper
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT

# Start with motor off
motor_on = False

# Get network information
try:
    from secrets import secrets
except ImportError:
    print("Secrets file could not be found.")
    raise

def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    print("Connected to Adafruit IO!")


def subscribe(client, userdata, topic, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print("Disconnected from Adafruit IO!")

# Assign pins for the motor functions
microstep_pins = (digitalio.DigitalInOut(board.D2),digitalio.DigitalInOut(board.D3),digitalio.DigitalInOut(board.D4))
step_pin = digitalio.DigitalInOut(board.D5)
dirn_pin = digitalio.DigitalInOut(board.D6)

step_pin.direction = digitalio.Direction.OUTPUT
dirn_pin.direction = digitalio.Direction.OUTPUT
dirn_pin.value = True

# Set motor to run with full steps
for pin in microstep_pins:
    pin.direction = digitalio.Direction.OUTPUT
    pin.value = False

# Run the the motor for 2000 steps
async def sstep(d):
    global motor_on
    if motor_on:
        for _ in range(1,2000):
            step_pin.value = True
            await asyncio.sleep(d)
            step_pin.value = False
            await asyncio.sleep(d)

# Get an update from Adafruit IO
async def update():
    try:
        io.loop()
    except (ValueError, RuntimeError) as e:
        print("Couldn't get data")
        wifi.reset()
        io.reconnect()

# Update the sensors (temperature and moisture sensors)
async def sensor_updates():
    moisture = get_moisture()
    temp = get_temp()

    io.publish("temperature", temp)
    io.publish("moisture", moisture)



# Set up SPI pins
esp32_cs = DigitalInOut(board.CS1)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

# Connect RP2040 to the WiFi module's ESP32 chip via SPI, then connect to WiFi
spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets)

# Assign pins for the sensors
moisture_sensor = AnalogIn(board.A0)
thermistor = AnalogIn(board.A1)

# Functions to get useful values of moisture level and temperature
def get_moisture():
    return moisture_sensor.value/420

def get_temp():
    return (55000-thermistor.value)/1000

# Function to handle the event that the pump is turned on through Adafruit IO
def on_pump_msg(client, topic, message):
    global motor_on
    if message == "ON":
        motor_on = True

    elif message == "OFF":
        motor_on = False
        step_pin.value = False

        print("off?")
    print(motor_on)
    print("?F?")

## Now that the setup is done, we can start.

# Connect to Wifi
print("Connecting to Wifi")
wifi.connect()
motor_on = False
print("Connected!")

# Create MQTT connection to Adafruit
MQTT.set_socket(socket, esp)

mqtt_client = MQTT.MQTT(
    broker="io.adafruit.com",
    port=secrets["port"],
    username=secrets["aio_username"],
    password=secrets["aio_key"],
)

io = IO_MQTT(mqtt_client)

io.on_connect = connected
io.on_disconnect = disconnected
io.on_subscribe = subscribe

# Push notification for change in pump value (on/off)
io.add_feed_callback("pump", on_pump_msg)

io.connect()
io.subscribe("pump")

# Async function main, so that all 3 of getting an update from Adafruit, turning the motor, and getting sensor values are done simultaneously.
async def main():
    prv_refresh_time = 0.0
    motor_refresh_time = 0.0
    while True:
        # Get Adafruit Update
        task1 = asyncio.create_task(update())
        # Turn the motor (check if motor_on = true in the sstep function)
        task2 = asyncio.create_task(sstep(0.0005))

        if (time.monotonic() - prv_refresh_time) > 5:
            # Get moisture level of the soil
            task3 = asyncio.create_task(sensor_updates())
            prv_refresh_time = time.monotonic()

        # Wait for task completion
        await asyncio.gather(task1, task2)

# Run the main loop
asyncio.run(main())
# Write your code here :-)
