#!/bin/bash
CMD=/Users/e1727/Dropbox/work/sumo/traffic-signal-control/main.py
source /Users/e1727/Dropbox/work/sumo/traffic-signal-control/.venv/bin/activate
export SUMO_HOME=/usr/share/sumo

C=1
DT=sq
DS=60
SR=1
SY=3
PA=../../data_generation
DW=0



cd f05
FREQ=0.5
# OPT="-c $C -i $DT -s $DS -p $PA -t $TH"
OPT="--nogui -c $C -i $DT -s $DS -p $PA --freq $FREQ"
python $CMD $OPT 

# cd f01
# FREQ=0.1
# # OPT="-c $C -i $DT -s $DS -p $PA -t $TH"
# OPT="--nogui -c $C -i $DT -s $DS -p $PA --freq $FREQ"
# python $CMD $OPT
# cd ..
# cd f03
# FREQ=0.3
# # OPT="-c $C -i $DT -s $DS -p $PA -t $TH"
# OPT="--nogui -c $C -i $DT -s $DS -p $PA --freq $FREQ"
# python $CMD $OPT
# cd ..
# cd f05
# FREQ=0.5
# # OPT="-c $C -i $DT -s $DS -p $PA -t $TH"
# OPT="--nogui -c $C -i $DT -s $DS -p $PA --freq $FREQ"
# python $CMD $OPT
# cd ..
# cd f07
# FREQ=0.7
# # OPT="-c $C -i $DT -s $DS -p $PA -t $TH"
# OPT="--nogui -c $C -i $DT -s $DS -p $PA --freq $FREQ"
# python $CMD $OPT
# cd ..
# cd f09
# FREQ=0.9
# # OPT="-c $C -i $DT -s $DS -p $PA -t $TH"
# OPT="--nogui -c $C -i $DT -s $DS -p $PA --freq $FREQ"
# python $CMD $OPT
# cd ..
