#!/bin/bash

p1=`seq 1 1`
p2=`seq 5 5`
p3=`seq 4 4`
for p1int in $p1 ;do
	for p2int in $p2 ;do
		for p3int in $p3 ;do
			cd ~/tarballs21/ns-allinone-3.29/ns-3.29
			rm src/dash/model/algorithms/data/*
			echo 2 > src/dash/model/algorithms/data/permission
			{ cd src/dash/model/algorithms/coma; conda activate torch; timeout 1800  python time_train_mc.py 3 $p1int $p2int $p3int; } &
			conda deactivate
			timeout 1800 ./waf --run 'src/dash/examples/dash-time --protocol="ns3::TimeClient" --stopTime=3017 --linkRate=3Mbps --users=3 --randomSeed=3' &
			wait
			mv src/dash/model/algorithms/results/logtime* src/dash/model/algorithms/coma/data/
		done
	done
done

cd ~/tarballs21/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/coma/
./testmodel.sh
