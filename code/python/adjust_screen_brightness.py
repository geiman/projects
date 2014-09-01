#! /usr/bin/env python
## Simple python app to increase screen brightness

import sys, argparse

current_brightness = int(0);
new_brightness = 0;
key = 0;

#f.write(new_brightness);

def read_brightness():
    global current_brightness
    global f
    current_brightness = int(f.readline());

def set_brightness():
    global current_brightness
    global new_brightness
    if (current_brightness + 1000) < 16055:
        f.write(new_brightness = str(current_brightness + 1000))

## Script Body

def main(argv):
    f = open('/sys/class/backlight/gmux_backlight/brightness', 'r+')
    parser = argparse.ArgumentParser(description='Increases or decreases screen brightness')
    parser.add_argument('key', metavar='k', type=int, help='A keyboard key number')

    args = parser.parse_args()
    print args.key

if __name__ == "__main__":
    main(sys.argv[1:])
