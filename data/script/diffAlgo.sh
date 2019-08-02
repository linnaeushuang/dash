#!/bin/bash

cd ~
mkdir -p diifAlgo/same/bus_13


rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/results/*
cd ~/tarballs/ns-allinone-3.29/ns-3.29

timeout 1800 ./waf --run 'src/dash/examples/dash-example --traceName=norway_bus_13 --randomSeed=3 --users=4 --linkRate=4Mbps --protocol="ns3::PensieveClient,ns3::BbClient,ns3::MpcClient,ns3::MpcfastClient"' &
sleep 17s
{ cd src/dash/model/algorithms; timeout 1800 python2.7 rl_no_training_mul.py 1 bus_13 72;  } &
wait
cp ./src/dash/model/algorithms/results/log_bus_13_* ~/diffAlgo/same/bus_13/


