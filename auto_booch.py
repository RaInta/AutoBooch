#!/usr/bin/python

##################################################
# 
# File: auto_booch.py
#
# Description: controls a heating pad via a DS18B20 
# thermal probe to optimize brewing of kombucha.
# You may have to change the number related to the 
# serial number of your particular device, as this 
# is uniquely assigned per probe. The current
# optimal temperature range is set between 24 and 
# 27 degrees Celcius.
#
# Created: 10 November 2017, Ra Inta
# Modifed: 20180326, R.I.
# Licence terms: Creative Commons 
# Attribution-ShareAlike 2.5 Generic 
# https://creativecommons.org/licenses/by-sa/2.5/
#
##################################################


import RPi.GPIO as GPIO
import time
import glob
import os


PWD=os.getcwd()

##################################################
# Useful parameters
##################################################

# {Dis-,En-}able logging by setting the following to {0,1}:
enable_logging = 1
logFile = os.path.join(PWD, 'brew_log.txt')

# GPIO pin number to control heating pad
pin_number = 17

# Define minimum and maximum temperatures (deg. C)
min_temp = 24
max_temp = 27

# Serial prefix for DS1820 probe.
# Note: You *may* have to replace the '28' prefix
# with the serial number for your own probe.
ds1820_prefix = '28'

# Name of output file for state of switch
#heating_pad_state = os.path.join(os.getcwd(), 'heating_pad_state.txt')
heating_pad_state = os.path.join(PWD, 'heating_pad_state.txt')


##################################################


##################################################
# System-specific stuff for DS1820 temp probe. 
##################################################

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'

device_folder = glob.glob(base_dir + ds1820_prefix + '*')[0]
device_file = device_folder + '/w1_slave'

##################################################


##################################################
# Set up GPIO pins
##################################################

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin_number, GPIO.OUT)

##################################################


##################################################
# Get temperature definitions
# Note: the following is in degrees Celcius.
# For Fahrenheit, I have defined a conversion 
# here: degCtoF().
##################################################

def read_temp_raw():
    with open(device_file, 'r') as deviceFile:
        lines = deviceFile.readlines()
    return lines

def degCtoF(tempC):
    """Converts from degrees Celcius to Fahrenheit"""
    return tempC * 9.0 / 5.0 + 32.0

def read_temp():
    """Reads device file and returns temperature in deg. Celcius"""
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        return float(temp_string) / 1000.0

##################################################

##################################################
# Define switching state
##################################################

def switch_state(state):
    """This takes in the state we want the switch to
    be in ("ON" or "OFF") and tries to do so. It
    outputs this new state to the state file defined
    at the top."""
    if state == "ON":
        gpio_state = GPIO.LOW
    else:
        gpio_state = GPIO.HIGH
    try:
        GPIO.output(pin_number, gpio_state)
        print(state)
        with open(heating_pad_state,'w') as outFile:
            outFile.write(state)
        if enable_logging:
            with open(logFile,'a') as logger:
                timeStr = str(time.time()) + " "
                logger.write(timeStr + str(curr_temp) + " " + state + "\n")

    except KeyboardInterrupt:
        print "Aborted by user"
        # Reset GPIO settings
        GPIO.cleanup()

##################################################


##################################################
# Perform control actions
##################################################

curr_temp = read_temp()

if curr_temp <= min_temp:
    switch_state("ON")
elif curr_temp >= max_temp:
    switch_state("OFF")
else:
    print("An error seems to have occurred! Attempting to abort.")
    switch_state("OFF")
    exit(1)

##################################################
