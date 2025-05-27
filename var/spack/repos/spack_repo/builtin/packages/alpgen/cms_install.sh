#!/bin/bash

if [ $# -ne 1 ];
    then echo "Usage: cms_install.sh <prefix>" && exit 1
fi

i=$1

mkdir -p $i/bin
mkdir -p $i/alplib
cp zjetwork/zjet_*gen $i/bin/
cp wjetwork/wjet_*gen $i/bin/
cp phjetwork/phjet_*gen $i/bin/
cp Njetwork/Njet_*gen $i/bin/

cp 2Qphwork/2Qphgen $i/bin/
cp 2Qwork/2Qgen $i/bin/
cp 4Qwork/4Qgen $i/bin/

cp hjetwork/hjetgen $i/bin/
cp Njetwork/Njetgen $i/bin/
cp phjetwork/phjetgen $i/bin/

cp QQhwork/QQhgen $i/bin/
cp topwork/topgen $i/bin/
cp vbjetwork/vbjetgen $i/bin/

cp wcjetwork/wcjetgen $i/bin/
cp wjetwork/wjetgen $i/bin/
cp wphjetwork/wphjetgen $i/bin/
cp wphqqwork/wphqqgen $i/bin/
cp wqqwork/wqqgen $i/bin/

cp zjetwork/zjetgen $i/bin/
cp zqqwork/zqqgen $i/bin/

cp -R alplib/* $i/alplib/