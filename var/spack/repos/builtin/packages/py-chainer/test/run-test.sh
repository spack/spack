#!/bin/bash

$@

grep -q "\"epoch\": 20," log
if [ $? -eq 1 ]; then
  echo "ChainerMN Test Incomplete !"
  exit 1 
fi

array=()

while read line;do
  column1=`echo ${line} | cut --delim=" " -f 1`
  column2=`echo ${line} | cut --delim=" " -f 2`
  
  if [ ${column1} == "\"main/accuracy\":" ]; then
    column2=${column2%,}
    array=("${array[@]}" ${column2})
  fi
done < log 

abs1=`echo "scale=20; 1.0 - ${array[0]}" | bc`
abs1=${abs1#-}
echo "main/accuracy1  = ${abs1}"

abs20=`echo "scale=20; 1.0 - ${array[19]}" | bc`
abs20=${abs20#-}
echo "main/accuracy20 = ${abs20}"

if [ `echo "$abs1 > $abs20" | bc` == 1 ]; then
  echo "ChainerMN Test Passed !"
else
  echo "ChainerMN Test Failed!"
fi

