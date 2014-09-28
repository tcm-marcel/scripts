scripts
=======

fetch_imap
----------
This script downloads all emails from INBOX, which have
been stared, and tries to extract the MatNr from the 
subject. Then for theese a direcory with the MatNr 
is created, where all text-attachments are saved. 
Theese mails then get unflagged afterwards. 

VCDdump
-------
Python script for the Raspberry Pi dumping the Activity of GPIO pins
to a VCD file that can be read by e.g. GTKWave. 
First try, so the frequency is very low - but it works!
Next try will be implementing VCDdump in C and maybe vor RT-Linux. 
