# ATIS print

This script is for students at the KIT[1], who have access to an ATIS[2] account[3]. It takes one or more files as argument and prints them remotely on a defined printer in the ATIS.

## Usage

The order of parameters is completely irrelevant.

    .../ATIS_print [file(s)]* [-u user] [-p printer] [-n number-of-copies] [-r from to]

- **files:** Regular expressions and single files are allowed.
- **user:** Specify a user for printing. This will dominate the default, but not override it permanently. Like a one-time-ticket. Useful for quickly printing things for others.
- **printer:** Use given printer. Must be sw1, sw2, sw3 (monochrome) or farb1 (color).
- **number-of-copies:** Specify how many times the files should be printed. Use integers only.
- **-r from to:** Specify a page **r**ange using integers as `from` and `to`. Only pages within this range will be printed if this is used. Otherwise the whole file will be printed.

## Dependencies

It depends on basic applications which are default on most unix-like operating systems. Tested on Ubuntu Linux and OSX Mavericks. 

    bash, scp, ssh

## Contribution wishlist, ideas and bugs

- BUG: Files with same names in different directories in one atis\_print call cause problems.
- Allow to print more pages on one paper (like `-#p 4`, see `man lp`). Note that this has impact on the -r option, see [CUPS docs][pageranges]
- For text/code print jobs, allow to adjust the text size (like `--txt-size 8`)
- Allow to print one/two-sided (like `-nd` or `--no-duplex`, also long- or short-sided?)
- Create Install/setup scripts for easier usage (install i.e. to `~/bin/`)
- Create completion file for better terminal experience (bash, fish, ...) or/and a manpage
- User should only need to input the password one time

[1] Karlsruher Institute of Technology

[2] "Abteilung für technische Infrastruktur" (Studentenpool) at the KIT

[3] Those accounts have usernames like `s_user`. It's given to students of informatics and business informatics.

[pageranges]: http://cups.org/documentation.php/doc-1.7/options.html?Q=lpr#PAGERANGES
