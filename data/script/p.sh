#/bin/bash

cd ~/tarballs/ns-allinone-3.29/ns-3.29

./waf --run 'src/dash/examples/dash-example --stopTime=300 --users=3 --protocol="ns3::MpcClient" --linkRate=3Mbps --traceName=norway_tram_20' &
{ cd src/dash/model/algorithms; python mpc_mul.py 3; } &
wait
cp src/dash/model/algorithms/data/realBuffer[0-2] ~/data/difftrace/3Stram20/robustmpc
cp src/dash/model/algorithms/results/log_mpc_sim_mul_[0-2]_0 ~/data/difftrace/3Stram20/robustmpc


./waf --run 'src/dash/examples/dash-example --stopTime=300 --users=3 --protocol="ns3::BbClient" --linkRate=3Mbps --traceName=norway_tram_20' &
{ cd src/dash/model/algorithms; python bb_mul.py 3; } &
wait
cp src/dash/model/algorithms/data/realBuffer[0-2] ~/data/difftrace/3Stram20/bb
cp src/dash/model/algorithms/results/log_bb_sim_mul_[0-2]_0 ~/data/difftrace/3Stram20/bb


./waf --run 'src/dash/examples/dash-example --stopTime=300 --users=3 --protocol="ns3::MpcfastClient" --linkRate=3Mbps --traceName=norway_tram_20' &
{ cd src/dash/model/algorithms; python mpcfast_mul.py 3; } &
wait
cp src/dash/model/algorithms/data/realBuffer[0-2] ~/data/difftrace/3Stram20/fastmpc
cp src/dash/model/algorithms/results/log_mpcfast_sim_mul_[0-2]_0 ~/data/difftrace/3Stram20/fastmpc


./waf --run 'src/dash/examples/dash-example --stopTime=300 --users=3 --protocol="ns3::PensieveClient" --linkRate=3Mbps --traceName=norway_tram_20' &
{ cd src/dash/model/algorithms; python rl_no_training_mul.py 3; } &
wait
cp src/dash/model/algorithms/data/realBuffer[0-2] ~/data/difftrace/3Stram20/pensieve
cp src/dash/model/algorithms/results/log_rl_sim_mul_[0-2]_0 ~/data/difftrace/3Stram20/pensieve
