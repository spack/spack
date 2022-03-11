#!/bin/bash

# this still needs some thinking ..
#cd $(dirname ${BASH_SOURCE[0]})
#git checkout nersc-develop || { echo "can't checkout nersc-develop, uncommitted changes?" ; exit 1 ; }
#now=$(date -Iminutes)
#br="sleak/merge-at-${now}"
#echo "$now" >> update-log
#git checkout -b $br
#git fetch upstream >> update-log || { echo "fetch upstream failed" ; exit 1 ; }
#git merge upstream/develop >> update-log || { echo "merge failed" ; exit 1 ; }
#git push --set-upstream origin $br
#curl -X POST -H "Accept: application/vnd.github.v3+json" \
#  https://api.github.com/repos/NERSC/spack/pulls \
#  -d '{"head":"$br","base":"nersc-develop"}'
#
#echo "" >> update-log
