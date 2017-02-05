#!/bin/sh

# Compilers
compilers=(
    %gcc@5.4.0
    %intel@16.0.3
)

# Compilers
spack install gcc@4.9.4 %gcc@4.8.5
spack install gcc@5.4.0 %gcc@4.8.5
spack install gcc@6.3.0 %gcc@4.8.5
spack install llvm 	%gcc@4.8.5
spack install jdk 	%gcc@4.8.5
spack install bazel	%gcc@4.8.5
spack install maven	%gcc@4.8.5
spack install lua-jit	%gcc@4.8.5

# Tools: git, emacs
spack install git 	%gcc@4.8.5
spack install emacs 	%gcc@4.8.5

# MPI 
for compiler in "${compilers[@]}"
do
	spack install openmpi@2.0.1 	$compiler
	spack install openmpi@1.10.3 	$compiler
	spack install openmpi@1.6.5 	$compiler
	spack install mvapich2		$compiler
	spack install mpich		$compiler
done

# CUDA
spack install cuda@8.0.44 %gcc@5
spack install cuda@8.0.44 %intel@16
spack install cuda@7.5.18 %gcc@4.8.5
spack install cuda@7.5.18 %intel@15
