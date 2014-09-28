#!/usr/bin/env python
# encoding: utf-8

# Python 3
# @author Marcel Kost <marcel.kost@student.kit.edu>

"""
example for VCDdump
(c) Marcel Kost 2014
"""

import VCDdump

vcd = VCDdump('example.vcd', 'BCM')
vcd.add_var('GPIO00/02', 3, GPIO.PUD_UP)
#vcd.add_var('GPIO01/03', 5, GPIO.PUD_UP)
#vcd.add_var('GPIO04', 7, GPIO.PUD_UP)
#vcd.add_var('GPIO17', 11, GPIO.PUD_UP)
#vcd.add_var('GPIO21/27', 13, GPIO.PUD_UP)
#vcd.add_var('GPIO22', 15, GPIO.PUD_UP)
#vcd.add_var('GPIO10', 19, GPIO.PUD_UP)
#vcd.add_var('GPIO09', 21, GPIO.PUD_UP)
#vcd.add_var('GPIO11', 23, GPIO.PUD_UP)
#vcd.add_var('GPIO14', 8, GPIO.PUD_UP)
#vcd.add_var('GPIO15', 10, GPIO.PUD_UP)
#vcd.add_var('GPIO18', 12, GPIO.PUD_UP)
#vcd.add_var('GPIO23', 16, GPIO.PUD_UP)
#vcd.add_var('GPIO24', 18, GPIO.PUD_UP)
#vcd.add_var('GPIO25', 22, GPIO.PUD_UP)
#vcd.add_var('GPIO08', 24, GPIO.PUD_UP)
#vcd.add_var('GPIO07', 26, GPIO.PUD_UP)

vcd.start()

while
