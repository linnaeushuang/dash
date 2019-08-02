#!/bin/bash

for i in `seq 100 100 600` ;do
	cd ~/tarballs21/ns-allinone-3.29/ns-3.29
	rm src/dash/model/algorithms/data/*
	echo 2 > src/dash/model/algorithms/data/permission
	{ cd src/dash/model/algorithms/coma; conda activate torch; timeout 1200 python time_test_mc.py 3 1 5 4  $i; } &
	conda deactivate
	timeout 1200 ./waf --run 'src/dash/examples/dash-time --protocol="ns3::TimeClient" --stopTime=1017 --linkRate=3Mbps --users=3 --randomSeed=3' &
	wait
	mv src/dash/model/algorithms/results/logtime* src/dash/model/algorithms/coma/testdata/
done

