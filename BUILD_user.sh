#!/bin/sh


# Configuration


# Compilers

compilers=(
    %gcc@5.4.0
    %intel@16.0.3
)

# GCC (install GCC only once)

# spack install gcc@4.9.4
# spack install gcc@5.4.0
# spack install gcc@6.3.0

# Tools: git, emacs

spack install git %gcc@4.8.5

# JDK

spack install jdk

# Perl

spack install perl@5.24.0 %gcc@5.4.0

# LuaJIT

for compiler in "${compilers[@]}"
do
	spack install lua-jit $compiler
done

# Python

#spack install python@2.7.13 	%gcc@5.4.0
#spack install python@2.7.13 	%intel@16.0.3
#spack install python@3.6.0 	%gcc@5.4.0

# MPI 

for compiler in "${compilers[@]}"
do
	spack install openmpi@2.0.1 	$compiler
	spack install openmpi@1.10.3 	$compiler
	spack install openmpi@1.6.5 	$compiler
	spack install mvapich2		$compiler
	spack install mpich		$compiler
done

# Bazel
spack install bazel	%gcc@5.4.0

# CUDA
for compiler in "${compilers[@]}"
do
	spack install cuda@8.0.44 $compiler
	spack install cuda@7.5.18 $compiler
done

# R
# spack install r@3.3.2 %gcc@5.4.0
