#!/bin/bash

cd ~/tarballs/ns-allinone-3.29/ns-3.29

./waf --run 'scratch/tcp --users=3 --linkRate=6Mbps --intervalStep=10 --stopTime=1024' >~/tcp3u10i2t.txt &
./waf --run 'scratch/tcp --users=4 --linkRate=8Mbps --intervalStep=10 --stopTime=1024' >~/tcp4u10i2t.txt &
./waf --run 'scratch/tcp --users=5 --linkRate=10Mbps --intervalStep=10 --stopTime=1024' >~/tcp5u10i2t.txt &
./waf --run 'scratch/tcp --users=6 --linkRate=12Mbps --intervalStep=10 --stopTime=1024' >~/tcp6u10i2t.txt &
./waf --run 'scratch/tcp --users=7 --linkRate=14Mbps --intervalStep=10 --stopTime=1024' >~/tcp7u10i2t.txt &


