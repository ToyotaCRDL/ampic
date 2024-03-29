#!/bin/bash
CMD=/Users/e1727/Dropbox/work/sumo/traffic-signal-control/main.py
source /Users/e1727/Dropbox/work/sumo/traffic-signal-control/.venv/bin/activate
export SUMO_HOME=/usr/share/sumo

C=4
DT=sq
DS=7
SR=1
SY=3
# PA=../../data_generation
PA=$1
HORIZON=10
# DW=0


cd w00000
DW=0.0 # Weight coef
OPT="--nogui -c $C -i $DT -s $DS -p $PA -w $DW -r $HORIZON"
python $CMD $OPT
