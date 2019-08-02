#!/bin/bash

for i in `ls trace` ;do
	if [ ${i##*.} = "sh" ];then
		./trace/$i
	fi
done
echo "ok"
#
#TYPE=('same' 'diff')
#for t in ${TYPE[@]}
#do
#	for n in `seq 3` ;do
#		rm ~/newdata/$t/errorTrace.txt
#		for i in `ls ~/newdata/$t` ;do
#			cp ./in.py ~/newdata/$t/$i
#			cp ~/tarballs/ns-allinone-3.29/ns-3.29/src/dash/model/algorithms/test_sim_traces/"norway_"$i ~/newdata/$t/$i
#			python2.7 ~/newdata/$t/$i/in.py 50 200
#			if [ $? != 0 ];then
#				echo $i >> ~/newdata/$t/errorTrace.txt
#			fi
#		done
#		if [ -s "/home/hl/newdata/$t/errorTrace.txt" ];then
#			for e in `cat ~/newdata/$t/errorTrace.txt` ;do
#				./trace/$e".sh"
#				echo "${t} ${i}"
#			done
#		else
#			echo "${t} succeed"
#			break
#		fi
#	done
#done
#cp ./dataStaitistics.py ~/newdata/
#python2.7 ~/newdata/dataStaitistics.py
