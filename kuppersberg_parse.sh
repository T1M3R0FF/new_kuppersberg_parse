#!/bin/bash

URL=$1

cd /home/mio-welt/PycharmProjects/new_kuppersberg_parse
source venv/bin/activate
python3 parse_from_link.py "$URL"
deactivate 

