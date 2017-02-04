#!/bin/sh

compilers=(
    %gcc@5.4.0
    %intel@16.0.3
)

# Perl

spack install perl@5.24.0 %gcc@5.4.0
spack install perl@5.24.0 %intel@16.0.3 cflags="-fPIC"

# Python, R, Boost

for compiler in "${compilers[@]}"
do
spack install python@2.7.13 $compiler
spack install python@3.6.0  $compiler
spack install r@3.3.2 	    $compiler
spack install boost 	    $compiler
done
