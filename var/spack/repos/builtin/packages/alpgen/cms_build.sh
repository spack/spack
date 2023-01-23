#!/bin/bash
cd 2Qphwork; make gen; cd ..
cd 2Qwork; make gen; cd ..
cd 4Qwork; make gen; cd ..
cd hjetwork; make gen; cd ..
cd Njetwork; make gen; cd ..
cd QQhwork; make gen; cd ..
cd topwork; make gen; cd ..
cd vbjetwork; make gen; cd ..
cd wcjetwork; make gen; cd ..
cd wphjetwork; make gen; cd ..
cd wphqqwork; make gen; cd ..
cd wqqwork; make gen; cd ..
cd zqqwork; make gen; cd ..

cd phjetwork; make gen;
export USRF=120_180bin
make gen -f cmsMakefile
export USRF=180_240bin
make gen -f cmsMakefile
export USRF=20_60bin
make gen -f cmsMakefile
export USRF=240_300bin
make gen -f cmsMakefile
export USRF=300_5000bin  ##this has changed it was up to 7000
make gen -f cmsMakefile
export USRF=60_120bin
make gen -f cmsMakefile
cd ..

cd wjetwork; make gen;
export USRF=0ptw100
make gen -f cmsMakefile
export USRF=100ptw300
make gen -f cmsMakefile
export USRF=300ptw800
make gen -f cmsMakefile
export USRF=800ptw1600
make gen -f cmsMakefile
export USRF=1600ptw3200 #was not in 213 patch
make gen -f cmsMakefile
export USRF=3200ptw5000 #was not in 213 patch
make gen -f cmsMakefile
export USRF=VBFHiggsTo2Tau #was not in 213 patch
make gen -f cmsMakefile
export USRF=2j_vbf_inv #was not in 213 patch
make gen -f cmsMakefile
export USRF=3j_vbf_inv #was not in 213 patch
make gen -f cmsMakefile
export USRF=1600ptw #was not in 212 patch
make gen -f cmsMakefile
cd ..

cd zjetwork; make gen;
export USRF=0ptz100
make gen -f cmsMakefile
export USRF=100ptz300
make gen -f cmsMakefile
export USRF=300ptz800
make gen -f cmsMakefile
export USRF=800ptz1600
make gen -f cmsMakefile
export USRF=1600ptz3200 #was not in 213 patch
make gen -f cmsMakefile
export USRF=3200ptz5000 #was not in 213 patch
make gen -f cmsMakefile
export USRF=VBFHiggsTo2Tau
make gen -f cmsMakefile
export USRF=2j_vbf_inv #was not in 213 patch
make gen -f cmsMakefile
export USRF=3j_vbf_inv #was not in 213 patch
make gen -f cmsMakefile
export USRF=1600ptz #was not in 212 patch
make gen -f cmsMakefile
cd ..

cd Njetwork; make gen; #whole Njetwork was not in 213 patch
export USRF=100_160
make gen -f cmsMakefile
export USRF=100_180
make gen -f cmsMakefile
export USRF=140_180
make gen -f cmsMakefile
export USRF=140_5600
make gen -f cmsMakefile
export USRF=160_200
make gen -f cmsMakefile
export USRF=180_250
make gen -f cmsMakefile
export USRF=180_5600
make gen -f cmsMakefile
export USRF=200_250
make gen -f cmsMakefile
export USRF=20_100
make gen -f cmsMakefile
export USRF=20_80
make gen -f cmsMakefile
export USRF=250_400
make gen -f cmsMakefile
export USRF=400_5600
make gen -f cmsMakefile
export USRF=80_140
make gen -f cmsMakefile
cd ..