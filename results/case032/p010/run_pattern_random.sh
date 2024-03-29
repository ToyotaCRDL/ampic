
#!/bin/bash
source /Users/e1727/Dropbox/work/sumo/traffic-signal-control/.venv/bin/activate

cd data_generation
 python mknet.py
 make clean
 make sq.sumocfg PERIOD=0.12 SEED=6
cd ..
cd rand_seed1
./run.sh
echo "random done"
cd ..
cd pattern_seed1
./run.sh
echo "pattern done"
cd ..

cd data_generation
 python mknet.py
 make clean
 make sq.sumocfg PERIOD=0.12 SEED=7
cd ..
cd rand_seed2
./run.sh
echo "random done"
cd ..
cd pattern_seed2
./run.sh
echo "pattern done"
cd ..

cd data_generation
 python mknet.py
 make clean
 make sq.sumocfg PERIOD=0.12 SEED=8
cd ..
cd rand_seed3
./run.sh
echo "random done"
cd ..
cd pattern_seed3
./run.sh
echo "pattern done"
cd ..

cd data_generation
 python mknet.py
 make clean
 make sq.sumocfg PERIOD=0.12 SEED=9
cd ..
cd rand_seed4
./run.sh
echo "random done"
cd ..
cd pattern_seed4
./run.sh
echo "pattern done"
cd ..

cd data_generation
 python mknet.py
 make clean
 make sq.sumocfg PERIOD=0.12 SEED=10
cd ..
cd rand_seed5
./run.sh
echo "random done"
cd ..
cd pattern_seed5
./run.sh
echo "pattern done"
cd ..
