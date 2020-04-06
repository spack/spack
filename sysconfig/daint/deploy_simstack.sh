#!/bin/bash
set -x
set -e

# Deployment directory
BASE_DIR=/apps/hbp/ich002/hbp-spack-deployments
DEPLOYMENT_HOME=$BASE_DIR/softwares/$(date '+%d-%m-%Y')

mkdir -p $DEPLOYMENT_HOME
mkdir -p $DEPLOYMENT_HOME/sources
mkdir -p $DEPLOYMENT_HOME/install

export HOME=$DEPLOYMENT_HOME

# Clone spack repository
cd $DEPLOYMENT_HOME/sources
[[ -d spack ]] || git clone https://github.com/BlueBrain/spack.git -b pr/juelich-update

# Setup environment
export SPACK_ROOT=`pwd`/spack
export PATH=$SPACK_ROOT/bin:$PATH
source $SPACK_ROOT/share/spack/setup-env.sh

# Copy configurations
mkdir -p $SPACK_ROOT/etc/spack/defaults/cray/
cp $SPACK_ROOT/sysconfig/daint/* $SPACK_ROOT/etc/spack/defaults/cray/

# Directory for deployment
export SOFTS_DIR_PATH=$DEPLOYMENT_HOME/install

module swap PrgEnv-cray PrgEnv-intel
module load daint-mc

# PYTHON 2 packages
spack spec -Il neuron %intel ^python@2.7.15 ^mpich
spack install --dirty --keep-stage -v neuron %intel ^python@2.7.15 ^mpich

spack spec -Il neuron~mpi %intel ^python@2.7.15
spack install --dirty --keep-stage -v neuron~mpi %intel ^python@2.7.15

# PYTHON 3 packages
module load cray-python/3.6.5.7

neurodamus_deps="^python@3.6.5 ^synapsetool%gcc"
spack spec -Il neurodamus-hippocampus+coreneuron %intel $neurodamus_deps
for nd in neurodamus-hippocampus neurodamus-neocortex neurodamus-mousify
do
   spack install --keep-stage --dirty -v $nd+coreneuron %intel $neurodamus_deps
done

spack spec -Il neuron~mpi %intel ^python@3.6.5
spack install --dirty --keep-stage -v neuron~mpi %intel ^python@3.6.5

module swap PrgEnv-intel PrgEnv-gnu

spack spec -Il py-bluepy%gcc ^python@3.6.5
spack install --dirty --keep-stage -v py-bluepy%gcc ^python@3.6.5

spack spec -Il py-sonata-network-reduction%gcc ^python@3.6.5 ^zeromq%intel
spack install --dirty --keep-stage -v py-sonata-network-reduction%gcc ^python@3.6.5 ^zeromq%intel

spack spec -Il py-bluepyopt%gcc ^python@3.6.5 ^zeromq%intel
spack install --dirty --keep-stage -v py-bluepyopt%gcc ^python@3.6.5 ^zeromq%intel

# Re-generate modules
spack module tcl refresh --delete-tree -y
cd $DEPLOYMENT_HOME/install/modules/tcl/cray-cnl7-haswell
# Remove neuron%gcc from the PYTHONPATH in python pacakges to avoid conflicts with neuron%intel
find py* -type f -print0|xargs -0 sed -i '/PYTHONPATH.*\/neuron-/d'
# Remove autoloading of mpich in neuron/neurodamus since cray-mpich module is loaded by default in daint
find neuro* -type f -print0|xargs -0 sed -i '/module load mpich/d'

ln -s $DEPLOYMENT_HOME/install/modules/tcl/cray-cnl6-haswell $DEPLOYMENT_HOME/modules
chmod -R ugo-w $DEPLOYMENT_HOME
