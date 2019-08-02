#!/bin/bash


for i in `seq 12`;do
	find -name 'downloadTime.sh' | xargs perl -p -e 's|bus_13|car_'$i'|g' | sed -n 1,42p >./trace/'car_'$i'.sh'
	chmod +x ./trace/'car_'$i'.sh'
done

for i in `seq 23`;do
	find -name 'downloadTime.sh' | xargs perl -p -e 's|bus_13|bus_'$i'|g' | sed -n 1,42p >./trace/'bus_'$i'.sh'
	chmod +x ./trace/'bus_'$i'.sh'
done

for i in `seq 20`;do
	find -name 'downloadTime.sh' | xargs perl -p -e 's|bus_13|ferry_'$i'|g' | sed -n 1,42p >./trace/'ferry_'$i'.sh'
	chmod +x ./trace/'ferry_'$i'.sh'
done

for i in `seq 10`;do
	find -name 'downloadTime.sh' | xargs perl -p -e 's|bus_13|metro_'$i'|g' | sed -n 1,42p >./trace/'metro_'$i'.sh'
	chmod +x ./trace/'metro_'$i'.sh'
done

for i in `seq 21`;do
	find -name 'downloadTime.sh' | xargs perl -p -e 's|bus_13|train_'$i'|g' | sed -n 1,42p >./trace/'train_'$i'.sh'
	chmod +x ./trace/'train_'$i'.sh'
done

for i in `seq 56`;do
	find -name 'downloadTime.sh' | xargs perl -p -e 's|bus_13|tram_'$i'|g' | sed -n 1,42p >./trace/'tram_'$i'.sh'
	chmod +x ./trace/'tram_'$i'.sh'
done

