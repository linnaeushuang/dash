#!/bin/bash

cd ~
mkdir -p downloadTime/same/bus_13

rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/results/*
cd ~/tarballs/ns-allinone-3.29/ns-3.29

timeout 2400 ./waf --run 'src/dash/examples/dash-example --traceName=norway_bus_13 --users=7 --linkRate=7Mbps --protocol="ns3::PensieveClient" --intervalStep=10' &
sleep 23s
{ cd src/dash/model/algorithms; timeout 1800 python2.7 rl_no_training_mul.py 7 bus_13 216;  }&
wait
cp ./src/dash/model/algorithms/results/log_bus_13_* ~/downloadTime/same/bus_13/


