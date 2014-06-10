# This script downloads all emails from INBOX, which have
# been stared, and tries to extract the MatNr from the 
# subject. Then for theese a direcory with the MatNr 
# is created, where all text-attachments are saved. 
# Theese mails then get unflagged afterwards. 
#
# Python 3
#
# @author Marcel Kost <marcel.kost@student.kit.edu>

import sys
import os
import re
import getpass
import imaplib
import email

# -----------------------------------------------------

# IMAP configuration
imap_server = 'imap.kit.edu'
imap_port = 993
imap_user = 'u-Account from student.kit.edu';   # change username here!

# -----------------------------------------------------

# class for colored output
class printc:
	def normal(string):
		print(string)
	
	def ok(string):
		print('\033[92m' + string + '\033[0m')
	
	def info(string):
		print('\033[94m' + string + '\033[0m')
	
	def fail(string):
		print('\033[91m' + string + '\033[0m')
	
	def warning(string):
		print('\033[93m' + string + '\033[0m')
	
	def header(string):
		print('\033[95m' + string + '\033[0m')


# activate debug interface
imaplib.IMAP4.debug = imaplib.IMAP4_SSL.debug = 1

passwd = getpass.getpass()
 
connection = imaplib.IMAP4_SSL(imap_server, imap_port)
connection.login(imap_user, passwd)

# open INBOX
connection.select('INBOX')
# get all mails, which are flagged (stared)
typ, data = connection.sort('DATE', 'UTF-8', 'FLAGGED')

# go through mails
for mail_num in data[0].split():
	typ, mail_data = connection.fetch(mail_num, '(RFC822)')
	mail_byte = mail_data[0][1]
	
	# extract mail body
	mail = email.message_from_string(mail_byte.decode('utf-8'))
	
	# extract and decode subject
	subject_encoded = email.header.decode_header(mail['Subject'])[0]
	if subject_encoded[1] is not None:
		subject = str(subject_encoded[0], subject_encoded[1])
	else:
		subject = str(subject_encoded[0])
	
	# extract and decode sender
	sender_encoded = email.header.decode_header(mail['From'])[0]
	if sender_encoded[1] is not None:
		sender = str(sender_encoded[0], sender_encoded[1])
	else:
		sender = str(sender_encoded[0])
	
	printc.normal(sender + ': ' + subject)
	
	matnr = re.findall("\d{7}", subject)
	if matnr is None or len(matnr) < 1:
		printc.fail('    No MatNr found. ')
		continue
	else:
		matnr = matnr[0]
		printc.ok('    MatNr: ' + matnr)
	
	saved = 0
	for part in mail.walk():
		if part.get_content_maintype() != 'text':
			continue
		if part.get('Content-Disposition') is None:
			continue
		
		filename = part.get_filename()
		data = part.get_payload(decode=True)
		if not data:
			continue
		
		# generate directory with MatNr if it doesn't exist
		if not os.path.isdir(matnr):
			os.mkdir(matnr)
		
		# generate file with sender information if it doesn't exist
		if not os.path.isdir(matnr + '/from.txt'):
			f = open(matnr + '/from.txt', 'w')
			f.write(sender)
			f.close()
		
		# save file in this directory
		f = open(matnr + '/' + filename, 'wb')
		f.write(data)
		f.close()
		
		printc.info('    file ' + filename + ' saved. ')
		saved++
	
	if saved > 0:
		# also unflag this email
		connection.store(mail_num, '-FLAGS', '\\FLAGGED')
       
connection.close()
connection.logout()
