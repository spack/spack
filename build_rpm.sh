#!/bin/sh

compilers=(
    %gcc@5.4.0
    %intel@16.0.3
)

# Python

for compiler in "${compilers[@]}"
do
spack install python@2.7.13 $mpiler
spack install python@3.6.0  $compiler
spack install r@3.3.2 	    $compiler
spack install boost 	    $compiler
done
