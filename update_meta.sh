#!/bin/bash
# ---------------------------------
# Created by Konfido on 2020-07-23
# ---------------------------------


# fetch content
TT=$(osascript <<EOF
tell application "System Events"
	tell application "Typora" to activate
	# tell process "Typora"
	# 	click static text 1 of text area 1 of text area 1 of UI element 1 of scroll area 1 of group 1 of group 1 of front window
	# end tell
	key code 126 using command down		-- Command+Up (back to top)
	delay 0.1
	keystroke "a" using command down
	delay 0.1
	keystroke "c" using command down
	delay 0.1
	get the clipboard
end tell
EOF
)

dateTime=$(date +'%Y-%m-%d %T')
updatedText=$(echo $TT | tr '\r' '\n'| sed "s/\(updated:\).*/\1 $dateTime/")


# echo $updatedText > ~/Desktop/text.txt


osascript <<BBB
tell application "System Events"
	set the clipboard to "$updatedText"
	keystroke "v" using command down
end tell
BBB