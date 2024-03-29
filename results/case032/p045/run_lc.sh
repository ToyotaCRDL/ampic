
#!/bin/bash
source /Users/e1727/Dropbox/work/sumo/traffic-signal-control/.venv/bin/activate
cd data_generation
 python mknet.py
 make clean
 make sq.sumocfg PERIOD=0.45
cd ..
cd lc_s60
./clean_all.sh
./run.sh


