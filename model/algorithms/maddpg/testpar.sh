#!/bin/bash

p1=`seq 1 3`
p2=`seq 3 6`
for p1int in $p1 ;do
	for p2int in $p2 ;do
		for p1dec in `seq 0 2 9` ;do
			for p2dec in `seq 0 2 9` ;do
				cd ~/tarballs12/ns-allinone-3.29/ns-3.29
				rm src/dash/model/algorithms/data/*
				echo 2 > src/dash/model/algorithms/data/permission
				{ cd src/dash/model/algorithms/maddpg; source activate pypen; timeout 600 python time_train_conv.py 1 $p1int.$p1dec 0  $p2int.$p2dec; } &
				source activate base
				timeout 550 ./waf --run 'src/dash/examples/dash-time --protocol="ns3::TimeClient" --stopTime=1017 --linkRate=2.5Mbps --users=1 --randomSeed=3' &
				wait
				mv src/dash/model/algorithms/results/logtime0 src/dash/model/algorithms/maddpg/data0/logtime_${p1int}_${p1dec}_${p2int}_${p2dec}
			done
		done
	done

done

