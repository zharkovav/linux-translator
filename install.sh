#!/usr/bin/env bash

sudo apt-get update -y
sudo apt-get install python-pip python-pyside
sudo apt-get install xsel

sudo pip install python-xlib requests

sudo pip install -e .
