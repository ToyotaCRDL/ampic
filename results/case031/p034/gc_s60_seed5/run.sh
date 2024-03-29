#!/bin/bash
CMD=/Users/e1727/Dropbox/work/sumo/traffic-signal-control/main.py
source /Users/e1727/Dropbox/work/sumo/traffic-signal-control/.venv/bin/activate
export SUMO_HOME=/usr/share/sumo

C=4
DT=sq
DS=60
SR=1
SY=3
PA=../../data_generation
# DW=0


cd w00000
DW=0.0 # Weight coef
OPT="--nogui -c $C -i $DT -s $DS -p $PA -w $DW"
python $CMD $OPT
DW=0.0200 # Weight coef
OPT="--nogui -c $C -i $DT -s $DS -p $PA -w $DW"
python $CMD $OPT
cd ..
