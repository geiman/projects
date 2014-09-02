#! /usr/bin/env python
## Simple python application to increase or decrease screen brightness

import sys, argparse


def brighten_screen(current_brightness):
    """ Return our brighter screen value

    The current brightness value is passed in.  We take that value and
    determine the new brighter value.  We increase brightness by values of
    1000, and if we're less than or equal to that amount away from the maximum
    value (16055) we simply return the maximum value.
    """
    if (current_brightness + 1000) < 16055:
        new_brightness = str(current_brightness + 1000)
    else:
        new_brightness = 16055

    return new_brightness

def dim_screen(current_brightness):
    """ Return our dimmer screen value

    The current brightness value is passed in.  We take that value and
    determine the new dimmer value.  We decrease brightness by values of
    1000, and if we're less than or equal to that amount away from the minimum
    value (0) we simply return the minimum value.
    """
    if (current_brightness - 1000) > 0:
        new_brightness = str(current_brightness - 1000)
    else:
        new_brightness = 0

    return new_brightness


## Script Body

def main(argv):
    """ Our main method.

    Here, we parse the CLI arguments, open the sysfile for reading, determine
    which key was pressed, call the appropriate function, and finally set the
    correct brightness.
    """
    parser = argparse.ArgumentParser(description='Increases or decreases screen brightness')
    parser.add_argument('key', metavar='k', type=int, help='A keyboard key number')

    args= parser.parse_args()

    f = open('/sys/class/backlight/gmux_backlight/brightness', 'r+')
    current_brightness = int(f.readline());

    # 232 == lower; 233 == higher
    if args.key == 232:
        new_brightness = dim_screen(current_brightness)
    elif args.key == 233:
        new_brightness = brighten_screen(current_brightness)
    else:
        print "Key not accepted"
        new_brightness = -1

    if (new_brightness != -1):
        f.write(str(new_brightness))



if __name__ == "__main__":
    main(sys.argv[1:])
