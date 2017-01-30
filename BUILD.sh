#!/bin/sh

# Configuration


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

spack install lua-jit %gcc@5.4.0
spack install lua-jit %intel@16.0.3

# Python

#spack install python@2.7.13 	%gcc@5.4.0
#spack install python@2.7.13 	%intel@16.0.3
#spack install python@3.6.0 	%gcc@5.4.0

# MPI 

spack install openmpi	%gcc@5.4.0
spack install mvapich2	%gcc@5.4.0
spack install mpich	%gcc@5.4.0
spack install openmpi	%intel@16.0.3

# Bazel
spack install bazel	%gcc@5.4.0

# CUDA
spack install cuda@8.0.44 %gcc@5.4.0
spack install cuda@7.5.18 %gcc@5.4.0
spack install cuda@6.5.14 %gcc@4.8.5

# R
# spack install r@3.3.2 %gcc@5.4.0
