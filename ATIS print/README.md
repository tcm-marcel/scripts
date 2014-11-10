# ATIS print

This script is for students at the KIT[1], who have access to an ATIS[2] account[3]. It takes one or more files as argument and prints them remotely on a defined printer in the ATIS[2].

## Usage

    .../ATIS_print [file(s)]

- **files:** Regular expressions or single files are allowed. Currently, only filenames are allowed, no paths included.

## Dependencies

It depends on basic applications which are default on most unix-like operating systems. Tested on Ubuntu Linux and OSX Mavericks. 

    bash, scp, ssh

## Contribution/TODOs

- DONE: Support directories and multiple files.
- BUG: Files with spaces (and other special chars?) will not be printed.
- TODO: Allow to set up a number of copies (like `-# 42`)
- TODO: Allow paths in filenames
- TODO: Create Install/setup scripts for easier usage (install i.e. to `~/bin/`)

[1]: Karlsruher Institute of Technology

[2]: Abteilung für technische Infrastruktur Studentenpool at Karlsruher Institute for Technology (KIT)

[3]: Those accounts have usernames like `s_user`. It's given to students of informatics and information economy.
