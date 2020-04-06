#!/bin/bash

# pass the argument of partition
if [ "$1" == "" ]; then
    echo "Error : pass --cluster or --booster"
    exit 1
fi

module --force purge

system=
cnrn_variant=

while [ "$1" != "" ]; do
    case $1 in
        -c | --cluster)         shift
                                system=cluster
                                cnrn_variant=~knl
                                module load Architecture/Haswell
                                module load Stages/2019a
                                module load Intel/2019.5.281-GCC-8.3.0 IntelMPI/2019.6.154 HDF5
                                ;;
        -b | --booster )        system=booster
                                cnrn_variant=+knl
                                module load Architecture/KNL
                                module load Stages/2019a
                                module load Intel/2019.5.281-GCC-8.3.0 IntelMPI/2019.6.154 HDF5
                                ;;
        * )                     echo "Error : --cluster or --booster"
                                exit 1
    esac
    shift
done

set -e

# Deployment directory
date=$(date '+%d-%m-%Y')
DEPLOYMENT_HOME=/p/project/cvsk25/software-deployment/HBP/jureca-$system/$date
mkdir -p $DEPLOYMENT_HOME/sources

# Clone spack repository and setup environment
cd $DEPLOYMENT_HOME/sources
[[ -d spack ]] || git clone https://github.com/BlueBrain/spack.git -b pr/juelich-update

# Setup environment
export SPACK_ROOT=`pwd`/spack
export PATH=$SPACK_ROOT/bin:$PATH
source $SPACK_ROOT/share/spack/setup-env.sh

# Copy configurations
mkdir -p $SPACK_ROOT/etc/spack/defaults/linux/
cp $SPACK_ROOT/sysconfig/jureca-$system/* $SPACK_ROOT/etc/spack/defaults/linux/

# Directory for deployment
export SPACK_INSTALL_PREFIX=$DEPLOYMENT_HOME

module list

# Python 2 packages
spack spec -Il neuron %intel ^python@2.7.15
spack install --dirty --keep-stage -v neuron %intel ^python@2.7.15

spack spec -Il neuron~mpi %intel ^python@2.7.15
spack install --dirty --keep-stage -v neuron~mpi %intel ^python@2.7.15

# Python 3 packages
module load Python/3.6.8
module load SciPy-Stack/2019a-Python-3.6.8
module list

neurodamus_deps="^coreneuron$cnrn_variant ^python@3.6.8 ^synapsetool%gcc"
spack spec -Il neurodamus-hippocampus+coreneuron %intel $neurodamus_deps
for nd in neurodamus-hippocampus neurodamus-neocortex neurodamus-mousify
do
   spack install --keep-stage --dirty -v $nd+coreneuron %intel $neurodamus_deps
done

spack spec -Il neuron~mpi %intel ^python@3.6.8
spack install --dirty --keep-stage -v neuron~mpi %intel ^python@3.6.8

spack spec -Il py-bluepy%gcc ^python@3.6.8
spack install --dirty --keep-stage -v py-bluepy%gcc ^python@3.6.8

spack spec -Il py-sonata-network-reduction%gcc ^python@3.6.8 ^zeromq%intel
spack install --dirty --keep-stage -v py-sonata-network-reduction%gcc ^python@3.6.8 ^zeromq%intel

spack spec -Il py-bluepyopt%gcc ^python@3.6.8 ^zeromq%intel
spack install --keep-stage --dirty -v py-bluepyopt%gcc ^python@3.6.8 ^zeromq%intel

spack module tcl refresh --delete-tree -y
cd $DEPLOYMENT_HOME/modules/tcl/linux-centos7-haswell
find py* -type f -print0|xargs -0 sed -i '/PYTHONPATH.*\/neuron-/d'
