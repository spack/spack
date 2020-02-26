#!/bin/bash
#. ../../setup.sh

#spackLoadUnique tasmanian
spack load tasmanian
#spackLoadUnique openblas threads=openmp

#spack load openblas threads=openmp
#spack load tasmanian@6.0 #+python
#spack load mpich
