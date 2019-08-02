#!/bin/bash

rm ../data/*
echo 3 >>../data/permission
python time_test_mc.py 2 1 5 4 50
