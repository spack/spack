#!/bin/sh

function s {
	spack find $@ | grep 'No package'
	if [ $? -eq 0 ]
	then
		spack install $@
	else
		echo "$@ has been installed."
	fi
}

compilers=(
    %gcc@6.3.0
    %intel@17.0.1
)

mpis=(
    openmpi@2.0.2
    mvapich2@2.2
    mpich@3.2
    intel-parallel-studio@cluster.2017
)

mpipkgs=(
  fftw
)

icc='%intel@17'

# CUDA
s cuda@8.0.44 %gcc@5
s cuda@8.0.44 %intel@16
s cuda@7.5.18 %gcc@4.8.5
s cuda@7.5.18 %intel@15

# Perl, Python, R, Boost
for compiler in "${compilers[@]}"
do
s python@2.7.13 $compiler
s python@3.6.0  $compiler
s r@3.3.2	$compiler
s boost		$compiler
s perl		$compiler
s jdk		$compiler
s bazel		$compiler
s gradle	$compiler
done

# MPI and MPI-dependent Libraries
for compiler in "${compilers[@]}"
do
	for mpi in "${mpis[@]}"
	do
		s $mpi $compiler
		for pkg in "${mpipkgs[@]}"
		do
			if [[ $mpi == "mvapich2"* ]]; then
				s $pkg$compiler +mpi ^$mpi+debug
			elif [[ $mpi == "intel"* ]]; then
				echo ">>> Debug"
				s $pkg$icc +mpi ^$mpi
			else
				s $pkg$compiler +mpi ^$mpi
			fi
		done
	done
done

# Other packages
s sga %intel@17
s sga %gcc@5
s mdtest %gcc ^openmpi
s simul %gcc ^openmpi
s anaconda2 %gcc
s anaconda3 %gcc
