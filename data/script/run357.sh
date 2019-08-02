
#/bin/bash




# seed is 1

cd ~
mkdir -p newdata/same/3mbps/bb
mkdir -p newdata/same/3mbps/mpc
mkdir -p newdata/same/3mbps/mpcfast
mkdir -p newdata/same/3mbps/pensieve
mkdir -p newdata/same/5mbps/bb
mkdir -p newdata/same/5mbps/mpc
mkdir -p newdata/same/5mbps/mpcfast
mkdir -p newdata/same/5mbps/pensieve
mkdir -p newdata/same/7mbps/bb
mkdir -p newdata/same/7mbps/mpc
mkdir -p newdata/same/7mbps/mpcfast
mkdir -p newdata/same/7mbps/pensieve

mkdir -p newdata/diff/3mbps/bb 
mkdir -p newdata/diff/3mbps/mpc
mkdir -p newdata/diff/3mbps/mpcfast
mkdir -p newdata/diff/3mbps/pensieve
mkdir -p newdata/diff/5mbps/bb
mkdir -p newdata/diff/5mbps/mpc
mkdir -p newdata/diff/5mbps/mpcfast
mkdir -p newdata/diff/5mbps/pensieve
mkdir -p newdata/diff/7mbps/bb
mkdir -p newdata/diff/7mbps/mpc
mkdir -p newdata/diff/7mbps/mpcfast
mkdir -p newdata/diff/7mbps/pensieve

rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/results/*
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
cd ~/tarballs/ns-allinone-3.29/ns-3.29
./waf --run 'src/dash/examples/dash-example --randomSeed=1 --users=5 --linkRate=3Mbps --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=1 --users=5 --linkRate=3Mbps --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=1 --users=5 --linkRate=3Mbps --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=1 --users=5 --linkRate=3Mbps --protocol="ns3::PensieveClient"' &
sleep 17s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/same/3mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/same/3mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/same/3mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/same/3mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=1 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=1 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=1 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=1 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::PensieveClient"' &
sleep 60s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/diff/3mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/diff/3mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/diff/3mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/diff/3mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=1 --users=5 --linkRate=5Mbps --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=1 --users=5 --linkRate=5Mbps --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=1 --users=5 --linkRate=5Mbps --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=1 --users=5 --linkRate=5Mbps --protocol="ns3::PensieveClient"' &
sleep 17s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/same/5mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/same/5mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/same/5mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/same/5mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=1  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=1  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=1  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=1  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::PensieveClient"' &
sleep 60s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/diff/5mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/diff/5mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/diff/5mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/diff/5mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=1 --users=5 --linkRate=7Mbps --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=1 --users=5 --linkRate=7Mbps --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=1 --users=5 --linkRate=7Mbps --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=1 --users=5 --linkRate=7Mbps --protocol="ns3::PensieveClient"' &
sleep 17s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/same/7mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/same/7mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/same/7mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/same/7mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=1  --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=1  --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=1  --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=1  --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::PensieveClient"' &
sleep 60s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/diff/7mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/diff/7mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/diff/7mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/diff/7mbps/pensieve

mv ~/newdata ~/seed1



# seed is 2

cd ~
mkdir -p newdata/same/3mbps/bb
mkdir -p newdata/same/3mbps/mpc
mkdir -p newdata/same/3mbps/mpcfast
mkdir -p newdata/same/3mbps/pensieve
mkdir -p newdata/same/5mbps/bb
mkdir -p newdata/same/5mbps/mpc
mkdir -p newdata/same/5mbps/mpcfast
mkdir -p newdata/same/5mbps/pensieve
mkdir -p newdata/same/7mbps/bb
mkdir -p newdata/same/7mbps/mpc
mkdir -p newdata/same/7mbps/mpcfast
mkdir -p newdata/same/7mbps/pensieve

mkdir -p newdata/diff/3mbps/bb 
mkdir -p newdata/diff/3mbps/mpc
mkdir -p newdata/diff/3mbps/mpcfast
mkdir -p newdata/diff/3mbps/pensieve
mkdir -p newdata/diff/5mbps/bb
mkdir -p newdata/diff/5mbps/mpc
mkdir -p newdata/diff/5mbps/mpcfast
mkdir -p newdata/diff/5mbps/pensieve
mkdir -p newdata/diff/7mbps/bb
mkdir -p newdata/diff/7mbps/mpc
mkdir -p newdata/diff/7mbps/mpcfast
mkdir -p newdata/diff/7mbps/pensieve

rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/results/*
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
cd ~/tarballs/ns-allinone-3.29/ns-3.29
./waf --run 'src/dash/examples/dash-example --randomSeed=2 --users=5 --linkRate=3Mbps --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=2 --users=5 --linkRate=3Mbps --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=2 --users=5 --linkRate=3Mbps --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=2 --users=5 --linkRate=3Mbps --protocol="ns3::PensieveClient"' &
sleep 17s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/same/3mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/same/3mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/same/3mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/same/3mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=2 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=2 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=2 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=2 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::PensieveClient"' &
sleep 60s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/diff/3mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/diff/3mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/diff/3mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/diff/3mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=2 --users=5 --linkRate=5Mbps --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=2 --users=5 --linkRate=5Mbps --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=2 --users=5 --linkRate=5Mbps --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=2 --users=5 --linkRate=5Mbps --protocol="ns3::PensieveClient"' &
sleep 17s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/same/5mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/same/5mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/same/5mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/same/5mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=2  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=2  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=2  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=2  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::PensieveClient"' &
sleep 60s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/diff/5mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/diff/5mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/diff/5mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/diff/5mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=2 --users=5 --linkRate=7Mbps --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=2 --users=5 --linkRate=7Mbps --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=2 --users=5 --linkRate=7Mbps --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=2 --users=5 --linkRate=7Mbps --protocol="ns3::PensieveClient"' &
sleep 17s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/same/7mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/same/7mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/same/7mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/same/7mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=2  --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=2  --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=2  --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=2  --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::PensieveClient"' &
sleep 60s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/diff/7mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/diff/7mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/diff/7mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/diff/7mbps/pensieve

mv ~/newdata ~/seed2



# seed is 3

cd ~
mkdir -p newdata/same/3mbps/bb
mkdir -p newdata/same/3mbps/mpc
mkdir -p newdata/same/3mbps/mpcfast
mkdir -p newdata/same/3mbps/pensieve
mkdir -p newdata/same/5mbps/bb
mkdir -p newdata/same/5mbps/mpc
mkdir -p newdata/same/5mbps/mpcfast
mkdir -p newdata/same/5mbps/pensieve
mkdir -p newdata/same/7mbps/bb
mkdir -p newdata/same/7mbps/mpc
mkdir -p newdata/same/7mbps/mpcfast
mkdir -p newdata/same/7mbps/pensieve

mkdir -p newdata/diff/3mbps/bb 
mkdir -p newdata/diff/3mbps/mpc
mkdir -p newdata/diff/3mbps/mpcfast
mkdir -p newdata/diff/3mbps/pensieve
mkdir -p newdata/diff/5mbps/bb
mkdir -p newdata/diff/5mbps/mpc
mkdir -p newdata/diff/5mbps/mpcfast
mkdir -p newdata/diff/5mbps/pensieve
mkdir -p newdata/diff/7mbps/bb
mkdir -p newdata/diff/7mbps/mpc
mkdir -p newdata/diff/7mbps/mpcfast
mkdir -p newdata/diff/7mbps/pensieve

rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/results/*
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
cd ~/tarballs/ns-allinone-3.29/ns-3.29
./waf --run 'src/dash/examples/dash-example --randomSeed=3 --users=5 --linkRate=3Mbps --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=3 --users=5 --linkRate=3Mbps --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=3 --users=5 --linkRate=3Mbps --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=3 --users=5 --linkRate=3Mbps --protocol="ns3::PensieveClient"' &
sleep 17s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/same/3mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/same/3mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/same/3mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/same/3mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=3 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=3 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=3 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::MpcfastClient"' &
wait
# this is error
timeout 600 ./waf --run 'src/dash/examples/dash-example --randomSeed=3 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::PensieveClient"' &
sleep 60s
{ cd src/dash/model/algorithms; timeout 600 python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/diff/3mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/diff/3mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/diff/3mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/diff/3mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=3 --users=5 --linkRate=5Mbps --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=3 --users=5 --linkRate=5Mbps --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=3 --users=5 --linkRate=5Mbps --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=3 --users=5 --linkRate=5Mbps --protocol="ns3::PensieveClient"' &
sleep 17s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/same/5mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/same/5mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/same/5mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/same/5mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=3  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=3  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=3  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=3  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::PensieveClient"' &
sleep 60s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/diff/5mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/diff/5mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/diff/5mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/diff/5mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=3 --users=5 --linkRate=7Mbps --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=3 --users=5 --linkRate=7Mbps --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=3 --users=5 --linkRate=7Mbps --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=3 --users=5 --linkRate=7Mbps --protocol="ns3::PensieveClient"' &
sleep 17s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/same/7mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/same/7mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/same/7mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/same/7mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=3  --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=3  --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=3  --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=3  --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::PensieveClient"' &
sleep 60s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/diff/7mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/diff/7mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/diff/7mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/diff/7mbps/pensieve

mv ~/newdata ~/seed3



# seed is 4

cd ~
mkdir -p newdata/same/3mbps/bb
mkdir -p newdata/same/3mbps/mpc
mkdir -p newdata/same/3mbps/mpcfast
mkdir -p newdata/same/3mbps/pensieve
mkdir -p newdata/same/5mbps/bb
mkdir -p newdata/same/5mbps/mpc
mkdir -p newdata/same/5mbps/mpcfast
mkdir -p newdata/same/5mbps/pensieve
mkdir -p newdata/same/7mbps/bb
mkdir -p newdata/same/7mbps/mpc
mkdir -p newdata/same/7mbps/mpcfast
mkdir -p newdata/same/7mbps/pensieve

mkdir -p newdata/diff/3mbps/bb 
mkdir -p newdata/diff/3mbps/mpc
mkdir -p newdata/diff/3mbps/mpcfast
mkdir -p newdata/diff/3mbps/pensieve
mkdir -p newdata/diff/5mbps/bb
mkdir -p newdata/diff/5mbps/mpc
mkdir -p newdata/diff/5mbps/mpcfast
mkdir -p newdata/diff/5mbps/pensieve
mkdir -p newdata/diff/7mbps/bb
mkdir -p newdata/diff/7mbps/mpc
mkdir -p newdata/diff/7mbps/mpcfast
mkdir -p newdata/diff/7mbps/pensieve

rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/results/*
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
cd ~/tarballs/ns-allinone-3.29/ns-3.29
./waf --run 'src/dash/examples/dash-example --randomSeed=4 --users=5 --linkRate=3Mbps --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=4 --users=5 --linkRate=3Mbps --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=4 --users=5 --linkRate=3Mbps --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=4 --users=5 --linkRate=3Mbps --protocol="ns3::PensieveClient"' &
sleep 30s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/same/3mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/same/3mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/same/3mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/same/3mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=4 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=4 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=4 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=4 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::PensieveClient"' &
sleep 120s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/diff/3mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/diff/3mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/diff/3mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/diff/3mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=4 --users=5 --linkRate=5Mbps --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=4 --users=5 --linkRate=5Mbps --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=4 --users=5 --linkRate=5Mbps --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=4 --users=5 --linkRate=5Mbps --protocol="ns3::PensieveClient"' &
sleep 17s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/same/5mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/same/5mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/same/5mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/same/5mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=4  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=4  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=4  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=4  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::PensieveClient"' &
sleep 60s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/diff/5mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/diff/5mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/diff/5mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/diff/5mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=4 --users=5 --linkRate=7Mbps --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=4 --users=5 --linkRate=7Mbps --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=4 --users=5 --linkRate=7Mbps --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=4 --users=5 --linkRate=7Mbps --protocol="ns3::PensieveClient"' &
sleep 17s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/same/7mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/same/7mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/same/7mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/same/7mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=4  --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=4  --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=4  --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=4  --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::PensieveClient"' &
sleep 60s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/diff/7mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/diff/7mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/diff/7mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/diff/7mbps/pensieve

mv ~/newdata ~/seed4



# seed is 5

cd ~
mkdir -p newdata/same/3mbps/bb
mkdir -p newdata/same/3mbps/mpc
mkdir -p newdata/same/3mbps/mpcfast
mkdir -p newdata/same/3mbps/pensieve
mkdir -p newdata/same/5mbps/bb
mkdir -p newdata/same/5mbps/mpc
mkdir -p newdata/same/5mbps/mpcfast
mkdir -p newdata/same/5mbps/pensieve
mkdir -p newdata/same/7mbps/bb
mkdir -p newdata/same/7mbps/mpc
mkdir -p newdata/same/7mbps/mpcfast
mkdir -p newdata/same/7mbps/pensieve

mkdir -p newdata/diff/3mbps/bb 
mkdir -p newdata/diff/3mbps/mpc
mkdir -p newdata/diff/3mbps/mpcfast
mkdir -p newdata/diff/3mbps/pensieve
mkdir -p newdata/diff/5mbps/bb
mkdir -p newdata/diff/5mbps/mpc
mkdir -p newdata/diff/5mbps/mpcfast
mkdir -p newdata/diff/5mbps/pensieve
mkdir -p newdata/diff/7mbps/bb
mkdir -p newdata/diff/7mbps/mpc
mkdir -p newdata/diff/7mbps/mpcfast
mkdir -p newdata/diff/7mbps/pensieve

rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/results/*
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
cd ~/tarballs/ns-allinone-3.29/ns-3.29
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=3Mbps --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=3Mbps --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=3Mbps --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=3Mbps --protocol="ns3::PensieveClient"' &
sleep 30s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/same/3mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/same/3mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/same/3mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/same/3mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=3Mbps --intervalStep=5 --protocol="ns3::PensieveClient"' &
sleep 120s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/diff/3mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/diff/3mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/diff/3mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/diff/3mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=5Mbps --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=5Mbps --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=5Mbps --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=5Mbps --protocol="ns3::PensieveClient"' &
sleep 17s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/same/5mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/same/5mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/same/5mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/same/5mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=5  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=5  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=5  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=5  --users=5 --linkRate=5Mbps --intervalStep=5  --protocol="ns3::PensieveClient"' &
sleep 60s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/diff/5mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/diff/5mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/diff/5mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/diff/5mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=7Mbps --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=7Mbps --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=7Mbps --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=7Mbps --protocol="ns3::PensieveClient"' &
sleep 17s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/same/7mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/same/7mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/same/7mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/same/7mbps/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::BbClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::MpcClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::MpcfastClient"' &
./waf --run 'src/dash/examples/dash-example --randomSeed=5 --users=5 --linkRate=7Mbps --intervalStep=5  --protocol="ns3::PensieveClient"' &
sleep 60s
{ cd src/dash/model/algorithms; python2.7 rl_no_training_mul.py 5 none 64;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/diff/7mbps/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/diff/7mbps/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/diff/7mbps/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/diff/7mbps/pensieve

mv ~/newdata ~/seed5



