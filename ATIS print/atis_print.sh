#!/bin/bash

### Configuration ############################################################
# specify ATIS account (s_xxx)
user="s_xxx"
# select ATIS printer to use (sw1/sw2/sw3 (monochrome) or farb1 (color))
printer="sw3"
##############################################################################

### Known bugs ###############################################################
# - Files with spaces or other special chars will not be printed.
# - Files with same names in different directories in one atis\_print call
#   cause problems.
##############################################################################


### Parse arguments ##########################################################
# This supports regular expressions and multiple files.
# Also supports options -u (user) and -p (printer).
# Invalid input will be ignored.
# Example: ./atis_print file1 file2 directory/* -u s_muster -p sw2
fpaths=		#file paths
fnames=		#file names
fcount=0	#amount of files to be printed
skipNum=0	#amount of invalid parameters

stage() {
	fpaths+=" $1"
	fnames+=" $(basename $1)"
	let "fcount += 1"
}

while (test $# -gt 0); do
	if (test -f $1) then
		stage $1
		shift
	elif (test $1 = "-u") && (test "$2" != "") then
		shift
		user=$1
		shift
	elif (test $1 = "-p";) && (test "$2" != "") then
		shift
		case $1 in
			sw1|sw2|sw3|farb1) 	printer=$1;;
			*)			let "skipNum += 1";;
		esac
		shift
	else
		#unknown parameter, skip it.
		let "skipNum += 1"
		#echo $1 #DEBUG
		shift
	fi
done
if (test -z "$fnames";) then
        echo "No file given"
        exit 1
fi
###############################################################################


### Review output && DEBUG options ############################################
if (test $skipNum -ne 0;) then
	echo "WARNING: $skipNum parameters are invalid and ignored."
fi
echo "This will print $fcount file(s) as \"$user\" on printer \"pool-$printer\""
echo "Files: $fpaths"
#echo "fnames: $fnames"	#DEBUG
#echo "scp $fpaths \"$user@i08fs1.ira.uka.de:~\""	#DEBUG
#echo "ssh -l $user i08fs1.ira.uka.de lpr -r -P pool-$printer $fnames"	#DEBUG
#exit 0	#DEBUG
echo "To abort, press CTRL+C when you are asked for the password."
###############################################################################


### Printing process ##########################################################
echo "Copy files to ATIS account: "
scp $fpaths "$user@i08fs1.ira.uka.de:~"
echo "Print files and delete copies on ATIS account: "
ssh -l $user i08fs1.ira.uka.de lpr -r -P pool-$printer $fnames
###############################################################################

