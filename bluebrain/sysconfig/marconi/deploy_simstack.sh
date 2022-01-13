#!/bin/bash
set -x
set -e

# Deployment directory
date=$(date '+%d-%m-%Y')

DEPLOYMENT_HOME=/marconi_work/HBP_CDP2_it/pkumbhar/HBP/marconi/$date
mkdir -p $DEPLOYMENT_HOME
mkdir -p $DEPLOYMENT_HOME/sources
mkdir -p $DEPLOYMENT_HOME/install

# Clone spack repository
cd $DEPLOYMENT_HOME/sources
[[ -d spack ]] || git clone https://github.com/BlueBrain/spack.git

# Setup environment
export SPACK_ROOT=`pwd`/spack
export PATH=$SPACK_ROOT/bin:$PATH
source $SPACK_ROOT/share/spack/setup-env.sh

# Copy configurations
mkdir -p $SPACK_ROOT/etc/spack/defaults/linux/
cp $SPACK_ROOT/sysconfig/marconi/* $SPACK_ROOT/etc/spack/defaults/linux/

# Setup directory for deployment
export SPACK_INSTALL_PREFIX=$DEPLOYMENT_HOME

# Clean environment and load python
module purge
module load gnu/7.3.0
module load intelmpi/2018--binary

# Python 2 packages
module load python/2.7.12
spack spec -Il neuron~mpi%gcc ^python@2.7.12
spack install --dirty --keep-stage -v neuron~mpi%gcc ^python@2.7.12

# python 3 packages
module swap python/2.7.12 python/3.6.4

spack spec -Il neuron~mpi%gcc ^python@3.6.4
spack install --dirty --keep-stage -v neuron~mpi%gcc ^python@3.6.4

spack spec -Il py-bluepyopt@1.9.12%gcc ^python@3.6.4 ^zeromq%intel
spack install --keep-stage --dirty -v py-bluepyopt@1.9.12%gcc ^python@3.6.4 ^zeromq%intel
spack install --keep-stage --dirty -v py-matplotlib%gcc ^python@3.6.4

# Change permissions
chmod -R g+rx $DEPLOYMENT_HOME
