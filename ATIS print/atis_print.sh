#!/bin/bash

### Configuration ############################################################
# specify ATIS account (s_xxx)
user="s_xxx"
# select ATIS printer to use (sw1/sw2/sw3 (monochrome) or farb1 (color))
printer="sw3"
# path to temporary directory for this script
dirTMP=/tmp/atis
##############################################################################

### Known bugs ###############################################################
# - Files with same names in different directories in one atis_print call
#   cause problems.
##############################################################################


### Parse arguments ##########################################################
fpaths=		#file paths (array)
fnames=		#file names (array)
fcount=0	#amount of files to be printed (integer)
skipNum=0	#amount of invalid parameters  (integer)
printNum=	#amount of copies for all given files (string)
pages=		#range of pages to print (for each file!) (string)
lowEnd=		#lower end of page range (see line above this one)
upperEnd=	#upper end of page range (see line above this one)
PDF=false	#return value of isPDF() $1 (boolean)

stage() {
	fpaths[$fcount]="$1"
	fnames[$fcount]="\"$(basename "$1")\""
	let "fcount += 1"
}

isPDF() {
        local info=`file -b "$1"`
        info=${info:0:3}
        if (test "$info" = "PDF") then
                PDF=true
        else
                PDF=false
        fi
}

#skip warns user about given parameters and counts them
skip() {
	let "skipNum += 1"
	echo "Ignore $@ (invalid/unknown option)"
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
		case "$2" in
			sw1|sw2|sw3|farb1) 	printer=$2;;
			*)			skip $1 $2;;
		esac
		shift; shift
	elif (test "$1" = "-n") && (test "$2" -gt 0) then
		shift
		printNum="-# $1"
		shift
	elif (test "$1" = "-r") && (test "$2" != "") && (test "$3" != "") then
		shift
		lowEnd=$1
		upperEnd=$2
		pages="-o page-ranges=$1-$2"
		shift
		shift
	elif (test "$1" = "-c") && (test "$2" -ge 2) then
		case "$2" in
			2|4|6|9)	compact="-o number-up=$2";;
			*)		skip $1 $2;;
		esac
		shift; shift
	else
		#unknown parameter -> ignore, warning message
		#directory -> ignore (no -r, use regular expressions instead)
		if !(test -d "$1";) then
			skip $1
		fi
		shift
	fi
done
if (test $fcount -le 0;) then
        echo "No file given"
        exit 1
fi
###############################################################################


### Review output #############################################################
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
echo "To abort, press CTRL+C when you are asked for the password."
###############################################################################


### Printing process ##########################################################
#first, if -r AND -c is used:
#create PDFs with the range given in -r
#and use those to print, so -r works with -c properly.
#Only do this if really necessary (-r in combination with -c is used)
#because this fix needs `pdfjam` as dependency and takes some time.
if (test "$pages" != "") && (test "$compact" != "") then
        mkdir $dirTMP
        for i in $(seq 0 ${#fpaths[@]})
                do
                isPDF "${fpaths[$i]}" #return value is $PDF
                if ($PDF) then
			#filter pdf pages and save to /tmp/atis/
			gs -sDEVICE=pdfwrite -q -dNOPAUSE -dBATCH -dSAFER \
				-dFirstPage=$lowEnd \
				-dLastPage=$upperEnd \
				-sOutputFile=$dirTMP/$(basename "${fpaths[$i]}") \
				"${fpaths[$i]}"

			# change filepath to filtered versions
                        fpaths[$i]=$dirTMP/$(basename "${fpaths[$i]}")
                fi
        done
fi

### DEBUG OPTIONS ##################
#echo "------- DEBUG INFOS --------"
#echo "FILENAMES: ${fnames[@]}"
#echo "FILEPATHS: ${fpaths[@]}"
#exit 0
####################################

# transfer and print
echo "Copy files to ATIS account: "
scp "${fpaths[@]}" "$user@i08fs1.ira.uka.de:~"
echo "Print files and delete copies on ATIS account: "
ssh -l $user i08fs1.ira.uka.de lpr -r -P pool-$printer $printNum $compact $pages "${fnames[@]}"
rm -rf $dirTMP
###############################################################################
