#! /usr/bin/env python
## Simple python app to increase screen brightness

import sys, argparse

#f.write(new_brightness);

#def set_brightness():
#    if (current_brightness + 1000) < 16055:
#        f.write(new_brightness = str(current_brightness + 1000))

def brighten_screen(current_brightness):
    if (current_brightness + 1000) < 16055:
        new_brightness = str(current_brightness + 1000)
    else:
        new_brightness = 16055

    return new_brightness

def dim_screen(current_brightness):
    if (current_brightness - 1000) > 0:
        new_brightness = str(current_brightness - 1000)
    else:
        new_brightness = 0

    return new_brightness


## Script Body

def main(argv):
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
