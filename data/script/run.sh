#/bin/bash



#for i in `ls trace` ;do
#	if [ ${i##*.} = "sh" ];then
#		./trace/$i
#	fi
#done
#echo "ok"

cd ~
mkdir -p newdata/same/bw2/bb
mkdir -p newdata/same/bw2/mpc
mkdir -p newdata/same/bw2/mpcfast
mkdir -p newdata/same/bw2/pensieve
mkdir -p newdata/diff/bw2/bb
mkdir -p newdata/diff/bw2/mpc
mkdir -p newdata/diff/bw2/mpcfast
mkdir -p newdata/diff/bw2/pensieve

mkdir -p newdata/same/bw5/bb
mkdir -p newdata/same/bw5/mpc
mkdir -p newdata/same/bw5/mpcfast
mkdir -p newdata/same/bw5/pensieve
mkdir -p newdata/diff/bw5/bb
mkdir -p newdata/diff/bw5/mpc
mkdir -p newdata/diff/bw5/mpcfast
mkdir -p newdata/diff/bw5/pensieve

mkdir -p newdata/same/bw3/bb
mkdir -p newdata/same/bw3/mpc
mkdir -p newdata/same/bw3/mpcfast
mkdir -p newdata/same/bw3/pensieve
mkdir -p newdata/diff/bw3/bb
mkdir -p newdata/diff/bw3/mpc
mkdir -p newdata/diff/bw3/mpcfast
mkdir -p newdata/diff/bw3/pensieve


rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/results/*
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*
cd ~/tarballs/ns-allinone-3.29/ns-3.29



timeout 1800 ./waf --run 'src/dash/examples/dash-example --users=3 --linkRate=2Mbps --protocol="ns3::BbClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --users=3 --linkRate=2Mbps --protocol="ns3::MpcClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --users=3 --linkRate=2Mbps --protocol="ns3::MpcfastClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --users=3 --linkRate=2Mbps --protocol="ns3::PensieveClient"' &
sleep 23s
{ cd src/dash/model/algorithms; timeout 1800 python2.7 rl_no_training_mul.py 3 none 72;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/same/bw2/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/same/bw2/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/same/bw2/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/same/bw2/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*

timeout 1800 ./waf --run 'src/dash/examples/dash-example --users=3 --linkRate=3Mbps --protocol="ns3::BbClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --users=3 --linkRate=3Mbps --protocol="ns3::MpcClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --users=3 --linkRate=3Mbps --protocol="ns3::MpcfastClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --users=3 --linkRate=3Mbps --protocol="ns3::PensieveClient"' &
sleep 23s
{ cd src/dash/model/algorithms; timeout 1800 python2.7 rl_no_training_mul.py 3 none 72;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/same/bw3/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/same/bw3/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/same/bw3/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/same/bw3/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*


timeout 1800 ./waf --run 'src/dash/examples/dash-example --users=3 --linkRate=5Mbps --protocol="ns3::BbClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --users=3 --linkRate=5Mbps --protocol="ns3::MpcClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --users=3 --linkRate=5Mbps --protocol="ns3::MpcfastClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --users=3 --linkRate=5Mbps --protocol="ns3::PensieveClient"' &
sleep 23s
{ cd src/dash/model/algorithms; timeout 1800 python2.7 rl_no_training_mul.py 3 none 72;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/same/bw5/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/same/bw5/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/same/bw5/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/same/bw5/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*


timeout 1800 ./waf --run 'src/dash/examples/dash-example --intervalStep=10 --users=3 --linkRate=2Mbps --protocol="ns3::BbClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --intervalStep=10 --users=3 --linkRate=2Mbps --protocol="ns3::MpcClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --intervalStep=10 --users=3 --linkRate=2Mbps --protocol="ns3::MpcfastClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --intervalStep=10 --users=3 --linkRate=2Mbps --protocol="ns3::PensieveClient"' &
sleep 23s
{ cd src/dash/model/algorithms; timeout 1800 python2.7 rl_no_training_mul.py 3 none 72;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/diff/bw2/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/diff/bw2/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/diff/bw2/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/diff/bw2/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*

timeout 1800 ./waf --run 'src/dash/examples/dash-example --intervalStep=10 --users=3 --linkRate=3Mbps --protocol="ns3::BbClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --intervalStep=10 --users=3 --linkRate=3Mbps --protocol="ns3::MpcClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --intervalStep=10 --users=3 --linkRate=3Mbps --protocol="ns3::MpcfastClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --intervalStep=10 --users=3 --linkRate=3Mbps --protocol="ns3::PensieveClient"' &
sleep 23s
{ cd src/dash/model/algorithms; timeout 1800 python2.7 rl_no_training_mul.py 3 none 72;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/diff/bw3/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/diff/bw3/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/diff/bw3/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/diff/bw3/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*


timeout 1800 ./waf --run 'src/dash/examples/dash-example --intervalStep=10 --users=3 --linkRate=5Mbps --protocol="ns3::BbClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --intervalStep=10 --users=3 --linkRate=5Mbps --protocol="ns3::MpcClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --intervalStep=10 --users=3 --linkRate=5Mbps --protocol="ns3::MpcfastClient"' &
timeout 1800 ./waf --run 'src/dash/examples/dash-example --intervalStep=10 --users=3 --linkRate=5Mbps --protocol="ns3::PensieveClient"' &
sleep 23s
{ cd src/dash/model/algorithms; timeout 1800 python2.7 rl_no_training_mul.py 3 none 72;  }&
wait
cp ./src/dash/model/algorithms/results/log_none_Bb* ~/newdata/diff/bw5/bb
cp ./src/dash/model/algorithms/results/log_none_Mpc_* ~/newdata/diff/bw5/mpc
cp ./src/dash/model/algorithms/results/log_none_Mpcfast* ~/newdata/diff/bw5/mpcfast
cp ./src/dash/model/algorithms/results/log_none_Pensieve* ~/newdata/diff/bw5/pensieve
rm ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/data/*

