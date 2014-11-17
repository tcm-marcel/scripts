# ATIS print

This script is for students at the KIT[1], who have access to an ATIS[2] account[3]. It takes one or more files as argument and prints them remotely on a defined printer in the ATIS.

## Usage

The order of parameters is completely irrelevant.

    .../ATIS_print [file(s)]* [-u user] [-p printer]

- **files:** Regular expressions and single files are allowed.
- **user:** Specify a user for printing. This will dominate the default, but not override it permanently. Like a one-time-ticket. Useful for quickly printing things for others.
- **printer:** Use given printer. Must be sw1, sw2, sw3 (monochrome) or farb1 (color).

## Dependencies

It depends on basic applications which are default on most unix-like operating systems. Tested on Ubuntu Linux and OSX Mavericks. 

    bash, scp, ssh

## Contribution/TODOs

- DONE: Support directories (as regular expression) and multiple files.
- FIXD: Files with spaces in filename or path will not be printed.
- BUG: Files with same names in different directories in one atis\_print call cause problems.
- TODO: Allow to set up a number of copies (like `-# 42`)
- DONE: Allow paths in filenames
- TODO: Create Install/setup scripts for easier usage (install i.e. to `~/bin/`)
- TODO: User should only need to input the password one time

[1] Karlsruher Institute of Technology

[2] "Abteilung für technische Infrastruktur" (Studentenpool) at the KIT

[3] Those accounts have usernames like `s_user`. It's given to students of informatics and business informatics.
