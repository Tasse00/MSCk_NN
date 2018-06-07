#!/bin/bash

result_dir=all_case_result

mkdir $result_dir 2>/dev/null

for c in 10 20 40 60 80 100 200 400 600 800 1000
do
    ./test $c | tee $result_dir/${c}.log | tail -n 2 > $result_dir/${c}.dat &
done

wait