#!/bin/sh

cc=%gcc@4.8.5

# Compilers
spack install gcc@4.9.4 $cc
spack install gcc@5.4.0 $cc
spack install gcc@6.3.0 $cc
spack install llvm 	$cc
spack install jdk 	$cc
spack install bazel	$cc
spack install maven	$cc
spack install lua-jit	$cc

# Tools: git, emacs
spack install git 	$cc	
spack install emacs 	$cc	
