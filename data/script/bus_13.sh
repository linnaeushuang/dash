#!/bin/bash

# seed is 3

cd ~
mkdir -p newdata/same/bus_13/bb
mkdir -p newdata/same/bus_13/mpc
mkdir -p newdata/same/bus_13/mpcfast
mkdir -p newdata/same/bus_13/pensieve
mkdir -p newdata/diff/bus_13/bb
mkdir -p newdata/diff/bus_13/mpc
mkdir -p newdata/diff/bus_13/mpcfast
mkdir -p newdata/diff/bus_13/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/results/*
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
cd ~/tarballs/ns-allinone-3.29/ns-3.29
timeout 1800 ./waf --run 'src/dash/examples/dash-example --traceName=norway_bus_13 --randomSeed=4 --users=5 --linkRate=5Mbps --protocol="ns3::BbClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --traceName=norway_bus_13 --randomSeed=4 --users=5 --linkRate=5Mbps --protocol="ns3::MpcClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --traceName=norway_bus_13 --randomSeed=4 --users=5 --linkRate=5Mbps --protocol="ns3::MpcfastClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --traceName=norway_bus_13 --randomSeed=4 --users=5 --linkRate=5Mbps --protocol="ns3::PensieveClient"' &
sleep 23s
{ cd src/dash/model/algorithms; timeout 1800 python2.7 rl_no_training_mul.py 5 bus_13 72;  }&
wait
cp ./src/dash/model/algorithms/results/log_bus_13_Bb* ~/newdata/same/bus_13/bb
cp ./src/dash/model/algorithms/results/log_bus_13_Mpc_* ~/newdata/same/bus_13/mpc
cp ./src/dash/model/algorithms/results/log_bus_13_Mpcfast* ~/newdata/same/bus_13/mpcfast
cp ./src/dash/model/algorithms/results/log_bus_13_Pensieve* ~/newdata/same/bus_13/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
timeout 1800 ./waf --run 'src/dash/examples/dash-example --traceName=norway_bus_13 --randomSeed=4 --users=5 --linkRate=5Mbps --intervalStep=5 --protocol="ns3::BbClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --traceName=norway_bus_13 --randomSeed=4 --users=5 --linkRate=5Mbps --intervalStep=5 --protocol="ns3::MpcClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --traceName=norway_bus_13 --randomSeed=4 --users=5 --linkRate=5Mbps --intervalStep=5 --protocol="ns3::MpcfastClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --traceName=norway_bus_13 --randomSeed=4 --users=5 --linkRate=5Mbps --intervalStep=5 --protocol="ns3::PensieveClient"' &
sleep 60s
{ cd src/dash/model/algorithms; timeout 1800  python2.7 rl_no_training_mul.py 5 bus_13 72;  }&
wait
cp ./src/dash/model/algorithms/results/log_bus_13_Bb* ~/newdata/diff/bus_13/bb
cp ./src/dash/model/algorithms/results/log_bus_13_Mpc_* ~/newdata/diff/bus_13/mpc
cp ./src/dash/model/algorithms/results/log_bus_13_Mpcfast* ~/newdata/diff/bus_13/mpcfast
cp ./src/dash/model/algorithms/results/log_bus_13_Pensieve* ~/newdata/diff/bus_13/pensieve

rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/results/*

