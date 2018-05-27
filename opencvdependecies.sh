#!/usr/bin/bash
sudo apt-get install libatlas-base-dev libjasper-dev libqtgui4 libqt4-test
sudo apt-get install python-virtualenv

virtualenv -p python3 env
source env/bin/activate
pip install --upgrade pip
pip install -r requeriments.txt
