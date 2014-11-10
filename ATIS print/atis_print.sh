#!/bin/bash

### Configuration ############################################################
# specify ATIS account (s_xxx)
user="s_xxx"
# select ATIS printer to use (sw1/sw2/sw3 (monochrome) or farb1 (color))
printer="sw3"
##############################################################################

### Known bugs ###############################################################
# - Files with spaces or other special chars will not be printed.
##############################################################################


### Search for valid files and store them in $files ###
# This supports regular expressions like ./* and multiple files as parameter
# but not directories like ./
# IMPORTANT: currently, files after a non-file parameter will be ignored.
files=
while (test $# -gt 0) && (test -f "$1")
        do
        files="$files $1"	#files separated with space
        shift
done
if test -z "$files"; then
        echo "No file given"
        exit 1
fi


echo "Copy files to ATIS account: "
scp $files "$user@i08fs1.ira.uka.de:~"


echo "Print files and delete copies on ATIS account: "
ssh -l $user i08fs1.ira.uka.de lpr -r -P pool-$printer $files
