#!/usr/bin/python
"""An implementation of a binary clock for the Beaglebone black"""
import sys
import time

import Adafruit_BBIO.GPIO as G

from datetime import datetime

## GPIO pin mapping to binary places
ONES = 'P8_8'
TWOS = 'P8_10'
FOURS = 'P8_12'
EIGHTS = 'P8_14'
HOURS_PINS = [ONES, TWOS, FOURS, EIGHTS]

AM_PM_PIN = 'P8_16'
ALL_PINS = HOURS_PINS + [AM_PM_PIN]


def clear_leds():
    # Flash the leds for fun
    for pin in ALL_PINS:
        G.setup(pin, G.OUT)
        G.output(pin, G.HIGH)

    time.sleep(1)
    for pin in ALL_PINS:
        G.output(pin, G.LOW)


def display_hour(now):
    hour = int(now.strftime('%I'))

    for pin in HOURS_PINS:
        is_pin_lit = hour & 1

        if is_pin_lit:
            G.output(pin, is_pin_lit)
        else:
            G.output(pin, G.HIGH)
            time.sleep(0.1)
            G.output(pin, G.LOW)

        hour >>= 1

    is_pm = now.strftime('%p') =='PM'
    G.output(AM_PM_PIN, is_pm)


def main():
    clear_leds()

    sys.stdout.write("Displaying current hour as\n")
    sys.stdout.flush()

    while True:
        now = datetime.now()
        display_hour(now)

        parsed_hour = now.hour % 12
        sys.stdout.write('%i' % parsed_hour)
        sys.stdout.flush()
        time.sleep(1)

        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)

        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)

        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)

        sys.stdout.write('\r    \r')
        sys.stdout.flush()


if __name__ == '__main__':
    main()

