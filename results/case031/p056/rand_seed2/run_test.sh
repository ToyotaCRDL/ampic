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


cd t001
TH=0.01
OPT="--nogui -c $C -i $DT -s $DS -p $PA -t $TH"
# OPT="--nogui -c $C -i $DT -s $DS -p $PA -t $TH --tls traffic_lights_log.csv"
python $CMD $OPT 
