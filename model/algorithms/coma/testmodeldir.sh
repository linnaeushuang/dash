#!/bin/bash

for i in `seq 4 11` ;do
	cd ~/tarballs21/ns-allinone-3.29/ns-3.29
	rm src/dash/model/algorithms/data/*
	rm src/dash/model/algorithms/results/*
	echo 2 > src/dash/model/algorithms/data/permission
	cd ~/tarballs21/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/coma/
	rm *pt
	cd testpardir
	./testpar$i.sh
done

