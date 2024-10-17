#!/bin/bash

if [ "$EUID" -ne 0 ]
then
    echo "Usage : sudo $0"
    exit
fi

cd /home/rpi/template_projet
source .venv/bin/activate
python capteur.py