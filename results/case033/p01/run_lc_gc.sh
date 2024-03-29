
#!/bin/bash
source /Users/e1727/Dropbox/work/sumo/traffic-signal-control/.venv/bin/activate

P=$(echo "scale=4; 1/0.1/5" | bc)
echo $P

cd data_generation
 python mknet.py
 make clean
 make sq.sumocfg PERIOD=$P SEED=1
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
 make sq.sumocfg PERIOD=$P SEED=2
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
 make sq.sumocfg PERIOD=$P SEED=3
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
 make sq.sumocfg PERIOD=$P SEED=4
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
 make sq.sumocfg PERIOD=$P SEED=5
cd ..
cd lc_s60_seed5
./run.sh
echo "local done"
cd ..
cd gc_s60_seed5
./run.sh
echo "global done"
cd ..
