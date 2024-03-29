
#!/bin/bash
source /Users/e1727/Dropbox/work/sumo/traffic-signal-control/.venv/bin/activate

cd data_generation_seed1
 make clean
 make sq.sumocfg PERIOD=0.23 SEED=1
cd ..

DATADIR='../../data_generation_seed1'
cd lc_s7_seed1
./run.sh $DATADIR
cd ..


cd data_generation_seed2
 make clean
 make sq.sumocfg PERIOD=0.23 SEED=2
cd ..

DATADIR='../../data_generation_seed2'
cd lc_s7_seed2
./run.sh $DATADIR
cd ..


cd data_generation_seed3
 make clean
 make sq.sumocfg PERIOD=0.23 SEED=3
cd ..

DATADIR='../../data_generation_seed3'
cd lc_s7_seed3
./run.sh $DATADIR
cd ..


cd data_generation_seed4
 make clean
 make sq.sumocfg PERIOD=0.23 SEED=4
cd ..

DATADIR='../../data_generation_seed4'
cd lc_s7_seed4
./run.sh $DATADIR
cd ..


cd data_generation_seed5
 make clean
 make sq.sumocfg PERIOD=0.23 SEED=5
cd ..

DATADIR='../../data_generation_seed5'
cd lc_s7_seed5
./run.sh $DATADIR
cd ..