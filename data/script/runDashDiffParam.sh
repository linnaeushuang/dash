cd ~/tarballs/ns-allinone-3.29/ns-3.29
./waf --run 'src/dash/examples/dash-example --users=5 --protocol="ns3::FdashClient" --linkRate=5120Kbps --stopTime=300 --maxBytes=100' >> src/dash/data/logFile/Log5_F_5120_100.txt
./waf --run 'src/dash/examples/dash-example --users=5 --protocol="ns3::FdashClient" --linkRate=5120Kbps --stopTime=300 --maxBytes=1024' >>src/dash/data/logFile/Log5_F_5120_1024.txt
./waf --run 'src/dash/examples/dash-example --users=5 --protocol="ns3::FdashClient" --linkRate=1024Kbps --stopTime=300 --maxBytes=1024' >>src/dash/data/logFile/Log5_F_1024_1024.txt
./waf --run 'src/dash/examples/dash-example --users=7 --protocol="ns3::FdashClient" --linkRate=1024Kbps --stopTime=300 --maxBytes=1024' >>src/dash/data/logFile/Log7_F_1024_1024.txt
./waf --run 'src/dash/examples/dash-example --users=7 --protocol="ns3::FdashClient" --linkRate=5120Kbps --stopTime=300 --maxBytes=1024' >>src/dash/data/logFile/Log7_F_5120_1024.txt
./waf --run 'src/dash/examples/dash-example --users=7 --protocol="ns3::FdashClient" --linkRate=5120Kbps --stopTime=300 --maxBytes=100' >>src/dash/data/logFile/Log7_F_5120_100.txt
sed -i '1,4d' src/dash/data/logFile/*.txt
