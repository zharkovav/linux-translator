# Linux translation

This package was created for translate selected text from 
English to Russian from every place in Linux system.

Usage is very straightforward: you run application (can work in
background), select text, press keyboard button (F2 by default) and
application pop-up window with selected text translation. Pop-up window
can be closed (hided actually) by pressing the Escape button.

For translate application uses lingualeo.com API and work simular
to their web-browser (at least Chrome) extension.

First version looks like this:

![linux-translate screenshot][screenshot]

[screenshot]: screenshot.png

# Installation

Application tested on Linux Ubuntu 14+.

Require: python2.7, xsel, PySide and python-xlib

To setup application run install.sh script.
To run type in console linux_translator command.

ToDo: add threads
