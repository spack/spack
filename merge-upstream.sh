#!/bin/bash

cd $(dirname ${BASH_SOURCE[0]})
git checkout nersc-develop || { echo "can't checkout nersc-develop, uncommitted changes?" ; exit 1 ; }
date >> update-log
git fetch upstream >> update-log || { echo "fetch upstream failed" ; exit 1 ; }
git merge upstream/develop >> update-log || { echo "merge failed" ; exit 1 ; }
echo "" >> update-log
