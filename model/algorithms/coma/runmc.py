#!/bin/bash

rm ../data/*
rm *pt
echo 3 >>../data/permission
python time_train_mc.py 1 1 0 4
