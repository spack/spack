#!/bin/bash
set -x
set -e

# Deployment directory
date=$(date '+%d-%m-%Y')

DEPLOYMENT_HOME=/gpfs/work/HBP_CDP21_it_1/pkumbhar/HBP/galileo/$date
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
cp $SPACK_ROOT/sysconfig/galileo/* $SPACK_ROOT/etc/spack/defaults/linux/

# Setup directory for deployment
export SPACK_INSTALL_PREFIX=$DEPLOYMENT_HOME

# Clean environment and load python
module purge
module load intel/pe-xe-2018--binary gnu/7.3.0
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

# matplotlib is external and python3
spack install --keep-stage --dirty -v py-matplotlib%gcc

spack module tcl refresh --delete-tree -y

# change permissions
chmod -R g+rx $DEPLOYMENT_HOME
