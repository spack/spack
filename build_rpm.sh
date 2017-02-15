#!/bin/sh

compilers=(
    %gcc@5.4.0
    %intel@16.0.4
)

mpis=(
    openmpi@1.6.5
    openmpi@1.10.3
    openmpi@2.0.2
    mvapich2@2.2
    mpich@3.2
)

# CUDA
spack install cuda@8.0.44 %gcc@5
spack install cuda@8.0.44 %intel@16
spack install cuda@7.5.18 %gcc@4.8.5
spack install cuda@7.5.18 %intel@15

# Perl
spack install perl@5.24.1 %gcc@5.4.0
spack install perl@5.24.1 %intel@16.0.4 cflags="-fPIC"

# Python, R, Boost
for compiler in "${compilers[@]}"
do
spack install python@2.7.13 $compiler
spack install python@3.6.0  $compiler
spack install r@3.3.2 	    $compiler
spack install boost 	    $compiler
done
