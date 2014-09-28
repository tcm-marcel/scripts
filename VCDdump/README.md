VCDdump
=======
Python script for the Raspberry Pi dumping the Activity of GPIO pins
to a VCD file that can be read by e.g. GTKWave. So it acts somehow like 
an binary Software Oscillator for the Raspberry Pi for debugging. 
First try, so the frequency is very low - but it works!
Next try will be implementing VCDdump in C and maybe for RT-Linux. 

Requirements
------------
* Python 3
* WiringPi

Usage
-----
Configure the pins to be dumped in example.py and then run it with
```
$ python3 example.py
```

Keywords
--------
Because this are the keywords I was searching with when hoping to find something like this...
* Raspberry Pi Oscillator
* Software Oscillator
* VCD Generator
* GTKWave Raspberry Pi
* Banana
