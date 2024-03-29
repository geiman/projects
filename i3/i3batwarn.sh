#!/bin/bash -x

#############################################
# This is a simple battery warning script.  #
# It uses i3's nagbar to display warnings.  #
#                                           #
# @author agribu <agribu[att]online[dott]de>#
#############################################

# lock file location
export LOCK_FILE=/tmp/battery_state.lock

# check if another copy is running
if [[ -a $LOCK_FILE ]]; then

    pid=$(cat $LOCK_FILE | awk '{print $1}')
	ppid=$(cat $LOCK_FILE | awk '{print $2}')
	# validate contents of previous lock file
	vpid=${pid:-"0"}
	vppid=${ppid:-"0"}

    if (( $vpid < 2 || $vppid < 2 )); then
		# corrupt lock file $LOCK_FILE ... Exiting
		cp -f $LOCK_FILE ${LOCK_FILE}.`date +%Y%m%d%H%M%S`
		exit
	fi

    # check if ppid matches pid
	ps -f -p $pid --no-headers | grep $ppid >/dev/null 2>&1

    if [[ $? -eq 0 ]]; then
		# another copy of script running with process id $pid
		exit
	else
		# bogus lock file found, removing
		rm -f $LOCK_FILE >/dev/null
	fi

fi

pid=$$
ps -f -p $pid --no-headers | awk '{print $2,$3}' > $LOCK_FILE
# starting with process id $pid

# set Battery
BATTERY=$(ls /sys/class/power_supply/ | grep '^BAT')

# set full path
ACPI_PATH="/sys/class/power_supply/$BATTERY"

# get battery status
STAT=$(cat $ACPI_PATH/status)

# get remaining energy value
REM=`grep "POWER_SUPPLY_ENERGY_NOW" $ACPI_PATH/uevent | cut -d= -f2`

# get full energy value
FULL=`grep "POWER_SUPPLY_ENERGY_FULL" $ACPI_PATH/uevent | grep -v "DESIGN" | cut -d= -f2`

# get current energy value in percent
PERCENT=`echo $(( $REM * 100 / $FULL ))`

# set error message
MESSAGE="AWW SNAP! I am running out of juice ...  Please, charge me or I'll have to power down."

# set energy limit in percent, where warning should be displayed
SOFTLIMIT="18"
HARDLIMIT="10"
SAVELIMIT="4"
#LIMIT="100"

# show warning if energy limit in percent is less then user set limit and
# if battery is discharging
if [ $PERCENT -le "$(echo $SOFTLIMIT)" ] && [ "$STAT" == "Discharging" ]; then
    if [ $PERCENT -le "$(echo $HARDLIMIT)" ] && [ "$STAT" == "Discharging" ]; then
    PID=`pidof -x i3-nagbar`

        if [[ -z "$PID" ]]; then
            DISPLAY=:0.0 /usr/bin/i3-nagbar -m "$(echo $MESSAGE)"
        else
            echo RUNNING
        fi
    fi
    notify-send -u critical "Battery Low ($PERCENT)"
fi
