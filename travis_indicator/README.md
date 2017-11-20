Ubuntu Travis Indicator
=======================

* Shows the most recent travis builds per repository and their status in the indicator menu
* Updates every 2 minutes and sends notifications for status changes
* A click on a build in the menu opens the job overview in the browser
* The status icon color shows if the last own build succeeded or not

![Screenshot](travis_indicator/screenshot.png?raw=true)

## Get Started
1. check `./travis_indicator.py` for required packets (all available via pip)
2. add Github token in `config.ini`
3. start indicator `./travis_indicator.py &`
