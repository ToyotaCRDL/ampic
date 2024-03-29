#!/bin/bash
CMD=/Users/e1727/Dropbox/work/sumo/traffic-signal-control/main.py
source /Users/e1727/Dropbox/work/sumo/traffic-signal-control/.venv/bin/activate
export SUMO_HOME=/usr/share/sumo

C=3
DT=sq
DS=60
SR=1
SY=3
PA=../../data_generation
DW=0

cd t00
TH=0.0
# OPT="-c $C -i $DT -s $DS -p $PA -t $TH"
OPT="--nogui -c $C -i $DT -s $DS -p $PA -t $TH"
python $CMD $OPT
