#!/bin/bash

### Configuration ############################################################
# specify ATIS account (s_xxx)
user="s_xxx"
# select ATIS printer to use (sw1/sw2/sw3 (monochrome) or farb1 (color))
printer="sw3"
##############################################################################

### Known bugs ###############################################################
# - Files with same names in different directories in one atis_print call
#   cause problems.
##############################################################################


### Parse arguments ##########################################################
# Example input: ./atis_print file1 file2 directory/* -u s_muster -p sw2
fpaths=		#file paths (array)
fnames=		#file names (array)
fcount=0	#amount of files to be printed (integer)
skipNum=0	#amount of invalid parameters  (integer)
printNum=	#amount of copies for all given files (string)
pages=		#range of pages to print (for each file!) (string)

stage() {
	fpaths[$fcount]="$1"
	fnames[$fcount]="\"$(basename "$1")\""
	let "fcount += 1"
}

while (test $# -gt 0); do
	if (test -f "$1") then
		stage "$1"
		shift
	elif (test "$1" = "-u") && (test "$2" != "") then
		shift
		user="$1"
		shift
	elif (test "$1" = "-p") && (test "$2" != "") then
		shift
		case "$1" in
			sw1|sw2|sw3|farb1) 	printer=$1;;
			*)			let "skipNum += 1";;
		esac
		shift
	elif (test "$1" = "-n") && (test "$2" -gt 0) then
		shift
		printNum="-# $1"
		shift
	elif (test "$1" = "-r") && (test "$2" != "") && (test "$3" != "") then
		shift
		pages="-o page-ranges=$1-$2"
		shift
		shift
	elif (test "$1" = "-c") && (test "$2" -ge 2) then
		shift
		case "$1" in
			2|4|6|9)	compact="-o number-up=$1";;
			*)		let "skipNum += 2";
		esac
		shift
	else
		#unknown parameter -> ignore, warning message
		#directory -> ignore (no -r, use regular expressions instead)
		if !(test -d "$1";) then
			let "skipNum += 1"
			echo "Ignore $1 (misused/unknown parameter)"
		fi
		shift
	fi
done
if (test $fcount -le 0;) then
        echo "No file given"
        exit 1
fi
###############################################################################


### Review output && DEBUG options ############################################
if (test $skipNum -ne 0;) then
	echo "WARNING: $skipNum parameters are invalid and ignored."
fi
if (test "$printNum" != "";) then
	echo "WARNING: This will print ${printNum:3} copies of every file!"
fi
echo "This will print $fcount file(s) as \"$user\" on printer \"pool-$printer\""
if (test "$pages" != "";) then
        echo "Print pages ${pages:15} of every file."
fi
echo "Files: ${fpaths[@]}"
#echo "fnames: ${fnames[@]}"	#DEBUG
#echo "scp ${fpaths[@]} \"$user@i08fs1.ira.uka.de:~\""	#DEBUG
#echo "ssh -l $user i08fs1.ira.uka.de lpr -r -P pool-$printer $printNum $compact $pages ${fnames[@]}"
#exit 0	#DEBUG
echo "To abort, press CTRL+C when you are asked for the password."
###############################################################################


### Printing process ##########################################################
echo "Copy files to ATIS account: "
scp "${fpaths[@]}" "$user@i08fs1.ira.uka.de:~"
echo "Print files and delete copies on ATIS account: "
ssh -l $user i08fs1.ira.uka.de lpr -r -P pool-$printer $printNum $compact $pages "${fnames[@]}"
###############################################################################
