
#!/bin/bash
source /Users/e1727/Dropbox/work/sumo/traffic-signal-control/.venv/bin/activate

cd data_generation
 python mknet.py
 make clean
 make sq.sumocfg PERIOD=0.89 SEED=6
cd ..
cd lc_s60_seed1
./run.sh
echo "local done"
cd ..
cd gc_s60_seed1
./run.sh
echo "global done"
cd ..

cd data_generation
 python mknet.py
 make clean
 make sq.sumocfg PERIOD=0.89 SEED=7
cd ..
cd lc_s60_seed2
./run.sh
echo "local done"
cd ..
cd gc_s60_seed2
./run.sh
echo "global done"
cd ..

cd data_generation
 python mknet.py
 make clean
 make sq.sumocfg PERIOD=0.89 SEED=8
cd ..
cd lc_s60_seed3
./run.sh
echo "local done"
cd ..
cd gc_s60_seed3
./run.sh
echo "global done"
cd ..

cd data_generation
 python mknet.py
 make clean
 make sq.sumocfg PERIOD=0.89 SEED=9
cd ..
cd lc_s60_seed4
./run.sh
echo "local done"
cd ..
cd gc_s60_seed4
./run.sh
echo "global done"
cd ..

cd data_generation
 python mknet.py
 make clean
 make sq.sumocfg PERIOD=0.89 SEED=10
cd ..
cd lc_s60_seed5
./run.sh
echo "local done"
cd ..
cd gc_s60_seed5
./run.sh
echo "global done"
cd ..
