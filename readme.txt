Note: as of 26 May 2015, this code is no longer being maintained.

Flash 2.0
A P-Roc project to convert a 1979 Williams Flash to a P-roc pinball machine.

The basic goal is to have the machine retain it's outward appearance, including the original plasma six digit displays, while replacing the aging MPU and driver boards with modern replacment that allow for custom programming.  As a side goal, the changes were intended to be completely reversable in case I found the need to pull the P-roc board, and use it in another project.


The hardware changes consist of a Proc board, and a custom Proc driver board intended for conversion of Williams system 11 machines.  More information on my hardware setup can be found here:  http://www.pinballcontrollers.com/forum/index.php?topic=1512.0

The diplay driver will be an Arduino Uno that I built and set up to take commands over USB.  The code for the board is posted here in the Adruino directory.  The board uses a pair of 74HC595s to drive the strobe inputs of the Williams system 3 to 6 display board.  The outputs on the Arduino are then used to drive a pair of four bit inputs on the Willisams board.  While I don't have a wiring diagram, you should be able to figure out what I did from my posting here:  http://www.pinballcontrollers.com/forum/index.php?topic=1429.msg12792#msg12792   There is also a picture of my finished board in this thread as well.
