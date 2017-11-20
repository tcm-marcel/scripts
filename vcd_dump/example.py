#!/usr/bin/env python
# encoding: utf-8

"""
example for VCDdump
(c) Marcel Kost 2014
"""

from VCDdump import VCDdump
import RPi.GPIO as GPIO

vcd = VCDdump('example.vcd', 'BCM')
vcd.add_var('GPIO00/02', 3, GPIO.PUD_UP)
vcd.add_var('GPIO01/03', 5, GPIO.PUD_UP)
vcd.add_var('GPIO04', 7, GPIO.PUD_UP)
vcd.add_var('GPIO17', 11, GPIO.PUD_UP)
vcd.add_var('GPIO21/27', 13, GPIO.PUD_UP)
vcd.add_var('GPIO22', 15, GPIO.PUD_UP)
vcd.add_var('GPIO10', 19, GPIO.PUD_UP)
vcd.add_var('GPIO09', 21, GPIO.PUD_UP)
vcd.add_var('GPIO11', 23, GPIO.PUD_UP)
vcd.add_var('GPIO14', 8, GPIO.PUD_UP)
vcd.add_var('GPIO15', 10, GPIO.PUD_UP)
vcd.add_var('GPIO18', 12, GPIO.PUD_UP)
vcd.add_var('GPIO23', 16, GPIO.PUD_UP)
vcd.add_var('GPIO24', 18, GPIO.PUD_UP)
vcd.add_var('GPIO25', 22, GPIO.PUD_UP)
vcd.add_var('GPIO08', 24, GPIO.PUD_UP)
vcd.add_var('GPIO07', 26, GPIO.PUD_UP)

print('preparing...')
vcd.start()
print('starting...')

try:
	while 1:
		pass
except KeyboardInterrupt:
	vcd.stop()
	del(vcd)
	
	exit()
