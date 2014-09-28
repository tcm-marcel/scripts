#!/usr/bin/env python
# encoding: utf-8

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
		self.vars[port] = (name, identifier, 0)
	
	def write_header(self):
		self.file.write("$date " + time.strftime("%c") + " $end\n")
		self.file.write("$version VCDdump for RaspberryPi 2014 $end\n")
		self.file.write("$timescale 1ps $end\n")
		
		self.file.write("$scope module RaspberryPi $end\n")
		self.file.write("$scope module " + self.module + " $end\n")
		
		for port, (name, identifier, last) in self.vars.items():
			self.file.write("$var reg 1 " + identifier + " " + name + " $end\n")
		
		self.file.write("$upscope $end\n")
		self.file.write("$upscope $end\n")
		self.file.write("$enddefinitions $end\n")
		self.file.write("#0\n")
		self.file.write("$dumpvars\n")
	
	def start(self):
		self.write_header()
		
		self.time_start = time.clock()
		self.time_last = self.time_start
		
		for port, (name, identifier, last) in self.vars.items():
			GPIO.remove_event_detect(port)
			GPIO.add_event_detect(port, GPIO.BOTH, callback=self.port_change)
			
			value = GPIO.input(port)
			self.vars[port] = (name, identifier, GPIO.input(port))
			self.format_value(identifier, value)
	
	def stop(self):
		for port, (name, identifier, last) in self.vars.items():
			GPIO.remove_event_detect(port)
		self.file.close()
		GPIO.cleanup()
	
	def port_change(self, port):
		time_current = time.clock()
		if time_current > self.time_last:
			self.time_last = time_current
			self.format_time(time_current)
			
		name, identifier, last = self.vars[port]
		value = GPIO.input(port)
		if value == last:
			return
		self.vars[port] = (name, identifier, value)
		self.format_value(identifier, value)
	
	def format_time(self, time_stamp):
		self.file.write("#" + str(int((time_stamp - self.time_start)*1000)) + "\n")
	
	def format_value(self, identifier, value):
		if value:
			self.file.write("0" + identifier + "\n")
		else:
			self.file.write("1" + identifier + "\n")
