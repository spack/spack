#!/bin/sh

compilers=(
    %gcc@5.4.0
    %intel@16.0.3
)

spack install zlib 	%gcc@5.4.0
spack install zlib 	%intel@16.0.3
