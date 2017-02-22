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
rm -f /home/rpm/spack/etc/spack/licenses/intel/license.lic; spack install intel-parallel-studio@cluster.2016.4 $cc +openmp 
rm -f /home/rpm/spack/etc/spack/licenses/intel/license.lic; spack install intel-parallel-studio@cluster.2015.6 $cc +openmp 
rm -f /home/rpm/spack/etc/spack/licenses/intel/license.lic; spack install intel-parallel-studio@cluster.2017.1 $cc +openmp 

# Tools: git, emacs
spack install git 	$cc	
spack install emacs 	$cc	
