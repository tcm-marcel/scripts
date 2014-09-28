VCDdump
=======
Python script for the Raspberry Pi dumping the Activity of GPIO pins
to a VCD file that can be read by e.g. GTKWave. 
First try, so the frequency is very low - but it works!
Next try will be implementing VCDdump in C and maybe vor RT-Linux. 

Usage
-----
Configure the pins to be dumped in example.py and then run it with
```
$ python3 example.py
```
