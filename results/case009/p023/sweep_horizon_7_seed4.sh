
#!/bin/bash
source /Users/e1727/Dropbox/work/sumo/traffic-signal-control/.venv/bin/activate

cd data_generation_seed4
 make clean
 make sq.sumocfg PERIOD=0.23 SEED=4
cd ..

DATADIR='../../data_generation_seed4'

cd gc_s7_horizon1_seed4
./run.sh $DATADIR
echo "global done"
cd ..
cd gc_s7_horizon2_seed4
./run.sh $DATADIR
echo "global done"
cd ..
cd gc_s7_horizon4_seed4
./run.sh $DATADIR
echo "global done"
cd ..
cd gc_s7_horizon6_seed4
./run.sh $DATADIR
echo "global done"
cd ..
cd gc_s7_horizon8_seed4
./run.sh $DATADIR
echo "global done"
cd ..
cd gc_s7_horizon10_seed4
./run.sh $DATADIR
echo "global done"
cd ..
