#!/bin/sh

# Configuration


# GCC (install GCC only once)

# spack install gcc@4.9.4
# spack install gcc@5.4.0
# spack install gcc@6.3.0

# Tools: git, emacs

spack install git

# JDK

spack install jdk

# Python

spack install python@2.7.13 %gcc@5.4.0
spack install python@3.6.0 %gcc@5.4.0

# MPI 

spack install opnmpi
spack install mvapich2
spack install mpich

# Bazel
spack install bazel

# R
# spack install r@3.3.2 %gcc@5.4.0
