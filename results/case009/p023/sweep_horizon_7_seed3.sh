
#!/bin/bash
source /Users/e1727/Dropbox/work/sumo/traffic-signal-control/.venv/bin/activate

cd data_generation_seed3
 make clean
 make sq.sumocfg PERIOD=0.23 SEED=3
cd ..

DATADIR='../../data_generation_seed3'
cd gc_s7_horizon1_seed3
./run.sh $DATADIR
echo "global done"
cd ..
cd gc_s7_horizon2_seed3
./run.sh $DATADIR
echo "global done"
cd ..
cd gc_s7_horizon4_seed3
./run.sh $DATADIR
echo "global done"
cd ..
cd gc_s7_horizon6_seed3
./run.sh $DATADIR
echo "global done"
cd ..
cd gc_s7_horizon8_seed3
./run.sh $DATADIR
echo "global done"
cd ..
cd gc_s7_horizon10_seed3
./run.sh $DATADIR
echo "global done"
cd ..
