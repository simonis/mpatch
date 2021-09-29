#!/bin/bash

fail=0

for i in `ls tests` ; do 
    mpatch "tests/$i/test" -o "tests/$i/check"
    echo "compare tests/$i/check tests/$i/out"
    diff -q "tests/$i/check" "tests/$i/out"
    if [ $? -ne 0 ]; then
        (( fail++ ))
    fi
done

if [ $fail -ne 0 ]; then
    echo "$fail tests failed"
fi
