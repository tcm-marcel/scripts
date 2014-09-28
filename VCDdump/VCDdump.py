#!/usr/bin/env python
# encoding: utf-8

# Python 3
# @author Marcel Kost <marcel.kost@student.kit.edu>

"""
Dumps the GPIO Ports from a raspberry pi to a VCD-file
(c) Marcel Kost 2014
"""

import string
import time
import RPi.GPIO as GPIO

identifiers = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '=', '>', '<', '-', '/', '*' ,'-', '+', '_', '{', '}', '[', ']', '~', '^', '°', '²', '³', '¼', '½', '¬']

class VCDdump:
	vars = {}
	time_last = 0
	
	def __init__(self, filename, module):
		self.module = module
		self.file = open(filename, 'w')
		
		GPIO.setmode(GPIO.BOARD)
	
	def __del__(self):
		self.file.close()
		GPIO.cleanup()

	def add_var(self, name, port, pud):
		GPIO.setup(port, GPIO.IN, pull_up_down=pud) # GPIO.PUD_UP / GPIO.PUD_DOWN
		identifier = identifiers.pop(0)
		vars[port] = (name, identifier)
	
	def write_header(self):
		self.file.write("$date " + time.strftime("%c") + " $end\n")
		self.file.write("$version VCDdump for RaspberryPi 2014 $end\n")
		self.file.write("$timescale 1ps $end\n")
		
		self.file.write("$scope module RaspberryPi $end\n")
		self.file.write("$scope module " + module + " $end\n")
		
		for port, (name, identifier) in self.vars.iteritems():
			self.file.write("$var reg 1 " + identifier + " " + name + " $end\n")
		
		self.file.write("$upscope $end\n")
		self.file.write("$upscope $end\n")
		self.file.write("$enddefinitions $end\n")
		self.file.write("#0\n")
		self.file.write("$dumpvars\n")
	
	def start():
		self.write_header()
		
		self.time_start = time.clock()
		self.time_last = self.time_start
		
		for port, (name, identifier) in self.vars.iteritems():
			GPIO.add_event_detect(port, GPIO.RISING, callback=port_rising)
			GPIO.add_event_detect(port, GPIO.FALLING, callback=port_falling)
	
	def stop():
		for port, (name, identifier) in self.vars.iteritems():
			GPIO.remove_event_detect(port)
	
	def check_port(self, port):
		if GPIO.input(port) == GPIO.HIGH:
			return 1
		else:
			return 0
	
	def port_rising(port):
		time = time.clock()
		if time > self.time_last:
			self.time_last = time
			self.file.write("#" + time + "\n")
		name, identifier = self.vars[port]
		self.file.write("1" + identifier + "\n")
	
	def port_falling(port):
		time = time.clock()
		if time > self.time_last:
			self.time_last = time
			self.file.write("#" + time + "\n")
		name, identifier = self.vars[port]
		self.file.write("0" + identifier + "\n")
