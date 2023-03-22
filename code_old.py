'''
ESC204 2022W Widget Lab 3IoT, Part 9
Task: Publish sensor data to Adafruit IO Dashboard using MQTT.
'''
# SPDX-FileCopyrightText: Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
from microcontroller import cpu
import board
import busio
import pwmio
import digitalio
from digitalio import DigitalInOut
from analogio import AnalogIn
from adafruit_motor import stepper
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT

motor_on = False
try:
    from secrets import secrets
except ImportError:
    print("Secrets file could not be found.")
    raise

def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    print("Connected to Adafruit IO! ")


def subscribe(client, userdata, topic, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))

# pylint: disable=unused-argument
def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print("Disconnected from Adafruit IO!")

microstep_pins = (digitalio.DigitalInOut(board.D2),digitalio.DigitalInOut(board.D3),digitalio.DigitalInOut(board.D4))
step_pin = digitalio.DigitalInOut(board.D5)
dirn_pin = digitalio.DigitalInOut(board.D6)

step_pin.direction = digitalio.Direction.OUTPUT
dirn_pin.direction = digitalio.Direction.OUTPUT

# set motor to run with full steps (not microsteps)
for pin in microstep_pins:
    pin.direction = digitalio.Direction.OUTPUT
    pin.value = False

def single_step(d):
    """
    Sends a pulse to the STEP output to actuate the stepper motor through one step.
    """
    # pulse high to drive step
    step_pin.value = True
    time.sleep(d)

    # bring low in between steps
    step_pin.value = False
    time.sleep(d)

# Set up SPI pins
esp32_cs = DigitalInOut(board.CS1)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

# Connect RP2040 to the WiFi module's ESP32 chip via SPI, then connect to WiFi
spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets)

# PIN SETUP HERE, with functions

moisture_sensor = AnalogIn(board.A0)


def get_moisture():
    return moisture_sensor.value/420

dirn_pin.value = True
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

#####
print("conectin gto wifi")
wifi.connect()
motor_on = False
print("connected")

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

#see if pump is on or off
io.add_feed_callback("pump", on_pump_msg)

io.connect()
io.subscribe("pump")

prv_refresh_time = 0.0
motor_refresh_time = 0.0

while True:
    try:
        io.loop()
    except (ValueError, RuntimeError) as e:
        print("Couldn't get data")
        wifi.reset()
        io.reconnect()
        continue

    if (time.monotonic() - prv_refresh_time) > 15:
        # get moisture level of the soil
        moisture = get_moisture()

        io.publish("moisture", moisture)
        prv_refresh_time = time.monotonic()
        print(motor_on)

    if (time.monotonic() - motor_refresh_time) > 0.5 and motor_on == True:
        for _ in range(0,200):
            single_step(0.002)

        motor_refresh_time = time.monotonic()
