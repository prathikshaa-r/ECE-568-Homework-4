#!/bin/bash
a=0
while [ $a -lt 10 ]
do
    python3 client.py $a
    let a++
done