# a4s_sealer_driver


## Description
A repository for Brooks XPeel, including user manuals and remote control interfaces.

This package guides a user to remotely control and receive feedback from the XPeel.

Peeler is the main object responsible for removing seals off of microplates
<p>&nbsp;</p>

## ROS2 Launch

### Sealer Client
 - `ros2 launch sealer_module_client sealer_module.launch.py`
 - Port name can be specified as `ros2 launch sealer_module_client sealer_module.launch.py sealer_port:=/dev/ttyUSB1`
### Peeler Client

 - `ros2 launch peeler_module_client peeler_module.launch.py`
 - Port name can be specified as `ros2 launch peeler_module_client peeler_module.launch.py peeler_port:=/dev/ttyUSB0`
## Current Features
* Peeler initialization
* Peeler information (version number, current status, tape remaining, etc.)
* Basic movements (move conveyor, spool, reset microplate, etc.)
* Execute peeling 
* Change sensor threshold value
* Displays up to 3 error messages at at ime
<p>&nbsp;</p>

## User Guide
1. ### Find and setup port
	* Connect XPeel Driver to device with a serial to usb cable.
	* Find XPeel port ex: "/dev/ttyUSB0" 
		In terminal:

			sudo sysctl kernel.dmesg_restrict=0
			dmesg | grep tty
		
		Example Response:

			[    0.132054] printk: console [tty0] enabled
			[    3.707958] usb 3-1: pl2303 converter now attached to ttyUSB0
			[ 9876.778770] pl2303 ttyUSB0: pl2303 converter now disconnected from ttyUSB0
			[ 9885.263688] usb 3-1: pl2303 converter now attached to ttyUSB0

		* Disconnect peeler

			  dmesg | grep tty
			
		Example Response:

			[    0.132054] printk: console [tty0] enabled
			[    3.707958] usb 3-1: pl2303 converter now attached to ttyUSB0
			[ 9876.778770] pl2303 ttyUSB0: pl2303 converter now disconnected from ttyUSB0

		* Compare difference to find port name
				
				sudo usermod -a -G dialout $USER
	

1. ### Git Clone azenta_driver repository
	In terminal:
	
		git clone https://github.com/AD-SDL/azenta_driver.git

2. ### Launching azenta driver on personal device

   In terminal:

        cd <azenta_driver location>
        cd azenta_driver
        touch __init__.py
        cd ..
        python setup.py
	
## Azenta Driver Send Command Guide

### Sending commands to XPeel driver:
	* Connect XPeel Driver to device with a serial to usb cable
	* Find XPeel port ex: "/dev/ttyUSB0"

   	In Python:
    
		from azenta_driver.peeler_driver import BROOKS_PEELER_CLIENT
		peeler = BROOKS_PEELER_CLIENT(port)

	* Send commands (provided below)
<p>&nbsp;</p>

## Azenta Driver Commands
### Commands for XPeel driver:
  * The peeler_driver.py file is responsible for sending commands for removing seals off of microplates
	   
1.     peeler.check_status()

Identifies up to 3 errors currently present.
<p>&nbsp;</p>

2.     peeler.check_version() 

Identifies the XPeel virmware version.
<p>&nbsp;</p>

3.     peeler.reset()

This command causes the spool to advance a few inches to fresh tape, and the elevator and conveyor axes to return to the home and ready for plate pick up position. A good use for the reset command is to ensure that fresh tape is presented after a long period of inactivity.
<p>&nbsp;</p>

4.     peeler.restart()

This command causes the XPeel to restart; the same as turning the power off and back on.
<p>&nbsp;</p>

5.     peeler.peel(Set Number, Time)

This command has a number of parameters that can be selected to achieve better performance on difficult or unusual seal types. For most seals the default and fastest settings will give good
performance. In an automated environment it may be advisable to be more conservative, or to provide
for a retry at slower settings when the XPeel detects that a seal is not removed.

Parameter sets 1-8 are fixed; parameter set 9 can be set and saved manually by the user.

| Set Number | Begin Peel Location | Speed  |
|------------|---------------------|--------|
| 1          | Default -2 mm       | fast   |
| 2          | Default -2 mm       | slow   |
| 3          | Default             | fast   |
| 4          | Default             | slow   |
| 5          | Default +2 mm       | fast   |
| 6          | Default +2 mm       | slow   |
| 7          | Default +4 mm       | fast   |
| 8          | Default +4 mm       | slow   |
| 9          | custom              | custom |


The second parameter, refers to adhere time in seconds.
<p>&nbsp;</p>

6.     peeler.seal_check()

The ‘sealcheck’ command causes the conveyor to place the plate under the reflective seal detection
sensor and the elevator to move down to the proper sensing elevation. The sensor status is then
recorded. The elevator and conveyor axes then return to the home and ready for plate pick up
position. Since this action only checks the plate at one location, a better indicator is the error code
that will be generated during a normal desealing operation where the plate is scanned over most of its
length. The ‘sealcheck’ command is useful, however, to verify that the sensor parameters are set
correctly to detect a particular seal type.
<p>&nbsp;</p>

7.     peeler.tape_remaining()

The XPeel calculates the amount of tape remaining on the supply spool by comparing the travel of the
conveyor to the rotation of both the supply and take-up spools. After a completed ‘XPeel’ operation, a
‘tapeleft’ command can be issued to verify the amount of tape left as well as the space remaining on
the take-up spool. These calculations are not perfectly accurate but they will provide sufficient
warning to avoid running out of tape unexpectedly.
<p>&nbsp;</p>

8.     peeler.plate_check(y or n?)

This command sets the plate check parameter to yes or no.
<p>&nbsp;</p>

9.     peeler.sensor_threshold()

This command reports the threshold value of the seal detected sensor.
<p>&nbsp;</p>

10.     peeler.sensor_threshold_higher(Threshold Value)

Setting the seal detected threshold value for the seal present if higher than threshold.

The Threshold Value refers to the 3 digit threshold value. This command sets the seal detected threshold so that during an XPeel, sensor readings higher than this value represents an un-removed seal and will
result in an error 04, “seal not removed”, message.
<p>&nbsp;</p>

11.     peeler.sensor_threshold_lower(Threshold Value)

Setting the seal detected threshold value for the seal present if lower than threshold.

Where Threshold Value refers to the 3 digit threshold value. This command sets the seal detected threshold so that during an XPeel, sensor readings lower than this value represents an un-removed seal and will
result in an error 04, “seal not removed”, message.
<p>&nbsp;</p>

12.     peeler.conveyor_out()

This command causes the conveyor to move out towards the user 7mm each time the command is called. When the conveyor reaches it’s fully extended home position no movement
occurs.
<p>&nbsp;</p>

13.     peeler.conveyor_in()

This command causes the conveyor to move in to the default ‘begin peel’ position.
<p>&nbsp;</p>

14.     peeler.elevator_down()

This command causes the elevator to move down until it is stopped by a plate or reaches its lower limit. The plate check option is disabled for this command.
<p>&nbsp;</p>

15.     peeler.elevator_up()

This command causes the elevator to move up approximately 1.5mm each time the
command is called until the elevator reaches it full up home position.
<p>&nbsp;</p>

16.     peeler.move_spool()

This command causes the spool to advance approximately 10mm of tape.

<p>&nbsp;</p>

## High Level Concepts
1. Peeler information is initialized
2. When a command is called a corresponding string is sent to the peeler.
3. The Peeler interprets this string and ouputs data/performs an action accordingly.
4. Python interprets output data from Peeler and displays messages while decoding error messages.
		
<p>&nbsp;</p>


## Python Dependencies
Code developed and tested with Python 3.9.12

Required packages:
* Serial Package Installation:

	    pip install pyserial
    
	    conda install pyserial

* Regex Package installation: 

        pip install regex


   In terminal:

