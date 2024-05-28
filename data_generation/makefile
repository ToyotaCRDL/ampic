# vehicle generation rate
PERIOD = 0.7
# random factor
RANDOMFACTOR = 1.2
# end time 
ETIME = 7200
SEED = 1395

DUAROUTER = $(SUMO_HOME)/bin/duarouter

OBJS = %.sumocfg %.net.xml %.rou.xml %.conn.csv %.edge.csv %.tls.csv %.nod.xml %.edg.xml %.priority_3way.yaml %.tmp.net.xml

.PRECIOUS: $(OBJS)

clean:
	rm -f *.sumocfg
	rm -f *.net.xml
	rm -f *.rou.xml
	rm -f *.rou.alt.xml
	rm -f *.nod.xml
	rm -f *.edg.xml
	rm -f *.priority_3way.yaml
	rm -f *.tmp.net.xml
	rm -f *.trips.xml
	rm -f tripinfo.xml
	
%.nod.xml: %.input.parsed
	touch $*.nod.xml

%.edg.xml: %.input.parsed
	touch $*.edg.xml
	
%.priority_3way.yaml: %.input.parsed
	touch $*.priority_3way.yaml
	
%.input.parsed: %.network.xml
	python src/to_xml.py --prefix $* \
			-e $(ETIME) \
			--period $(PERIOD)

%.tmp.net.xml: %.nod.xml %.edg.xml
	netconvert \
	--node-files=$*.nod.xml \
	--edge-files=$*.edg.xml \
	--output-file=$*.tmp.net.xml \
	--lefthand \
	--keep-edges.components 1 \
	--no-turnarounds \
	--tls.discard-simple \
	--tls.join

%.net.xml: %.tmp.net.xml %.priority_3way.yaml 
	python src/fix_tlLogic.py --prefix $*

%.rou.xml: %.net.xml %.input.parsed
	$(DUAROUTER) \
	--junction-taz \
	-v \
	--weights.random-factor "$(RANDOMFACTOR)" \
	-n $*.net.xml \
	-r $*.trips.xml \
	--seed $(SEED) \
	--begin 0 --end $(ETIME) \
	-o $*.rou.xml

%.sumocfg: %.rou.xml
	python src/make_sumocfg.py $*
