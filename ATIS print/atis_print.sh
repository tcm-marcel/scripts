#!/bin/bash

# so far only for SINGLE DOCUMENTS
# TODO: add feature to print several documents and whole directories

# specify ATIS account (s_xxx)
user="s_xxx"
# select ATIS print to use (sw1/sw2/sw3)
printer="sw3"

file="$1"

scp "$file" "$user@i08fs1.ira.uka.de:~"
ssh -l $user i08fs1.ira.uka.de lpr -r -P pool-$printer \"$file\"
