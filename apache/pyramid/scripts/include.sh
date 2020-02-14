#!/bin/bash

if [ $# -eq 0 ]; then
        echo "First argument must be environment (either dev or prod)"
        exit 1
fi

echo "Setting environmental variables for $1"

#Setting environmental variables
while IFS= read -r line
do
    export `echo $line | cut -d' ' -f1`=`echo $line | cut -d' ' -f2`
done < ../environments/$1
