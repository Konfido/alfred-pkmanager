#!/bin/bash
# ------------------------------------------------
# Author:        Konfido <konfido.du@outlook.com>
# Created Date:  July 23rd 2020
# ------------------------------------------------


# fetch content
TT=$(osascript <<EOF
tell application "System Events"
	tell front window of application "Typora" to activate
	keystroke "a" using command down
	delay 0.1
	keystroke "c" using command down
	delay 0.1
	get the clipboard
end tell
EOF
)

dateTime=$(date +'%Y-%m-%d %T')
updatedText=$(echo $TT | tr '\r' '\n'| sed "s/\(updated: \).*/\1$dateTime/")


# echo $updatedText > ~/Desktop/text.txt


osascript <<BBB
tell application "System Events"
	set the clipboard to "$updatedText"
	keystroke "v" using command down
end tell
BBB