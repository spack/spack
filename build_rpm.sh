#!/bin/sh

compilers=(
    %gcc@5.4.0
    %intel@16.0.3
)

# Python

spack install python@2.7.13 	%gcc@5.4.0
spack install python@2.7.13 	%intel@16.0.3
spack install python@3.6.0 	%gcc@5.4.0
spack install python@3.6.0 	%intel@16.0.3

# R
spack install r@3.3.2 %gcc@5.4.0
