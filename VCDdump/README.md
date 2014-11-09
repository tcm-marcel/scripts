VCDdump
=======
Python script for the Raspberry Pi dumping the Activity of GPIO pins
to a VCD file that can be read by e.g. GTKWave (http://gtkwave.sourceforge.net). So it acts somehow like 
an binary Software Oscilloscope for the Raspberry Pi for debugging. 
First try, so the frequency is very low - but it works!
Next try will be implementing VCDdump in C and maybe for RT-Linux. (and maybe using an AD-converter)

Requirements
------------
* Python 3
* WiringPi

Usage
-----
Configure the pins to be dumped in example.py and then run it with
```
$ sudo python3 example.py
```
Root required for pin access (WiringPi)

Related Work
------------
* pi-oscilloscope (https://github.com/ankitaggarwal011/pi-oscilloscope) uses an _ADS1015 Breakout board Analog to Digital converter_ and plots the data with python. (I haven't tried it yet)
	* Pro: It measures with 12 Bit instead of only binary.
	* Contra: I think it might be very slow as well. 
* Panalyzer (https://github.com/richardghirst/Panalyzer)

Keywords
--------
Because this are the keywords I was searching with when hoping to find something like this...
* Raspberry Pi Oscilloscope
* Software Oscilloscope
* VCD Generator
* GTKWave Raspberry Pi
