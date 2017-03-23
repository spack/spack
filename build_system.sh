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

cc=%gcc@4.8.5

compilers=(
    %gcc@6.3.0
    %intel@17.0.2
    %pgi@16.10
)

mpis=(
    openmpi@2.0.2
    mvapich2@2.2
    mpich@3.2
    intel-parallel-studio@cluster.2017.2+mpi
)

# Compilers
s pgi@16.10 $cc
s gcc@4.9.4 $cc
s gcc@5.4.0 $cc
s gcc@6.3.0 $cc
s llvm 	$cc
s jdk 	$cc
s gradle $cc
s ant $cc
s bazel	$cc
s maven	$cc
s lua-jit	$cc

rm -f /home/rpm/spack/etc/spack/licenses/intel/license.lic; s intel-parallel-studio@cluster.2015.6$cc +openmp+mpi+mkl+ipp
rm -f /home/rpm/spack/etc/spack/licenses/intel/license.lic; s intel-parallel-studio@cluster.2015.6%intel@15.0.6 +openmp+mpi+mkl+ipp

rm -f /home/rpm/spack/etc/spack/licenses/intel/license.lic; s intel-parallel-studio@cluster.2016.4$cc +openmp+mpi+mkl+ipp
rm -f /home/rpm/spack/etc/spack/licenses/intel/license.lic; s intel-parallel-studio@cluster.2016.4%intel@16.0.4 +openmp+mpi+mkl+ipp


rm -f /home/rpm/spack/etc/spack/licenses/intel/license.lic; s intel-parallel-studio@cluster.2017.2$cc +openmp+mpi+mkl+ipp 
rm -f /home/rpm/spack/etc/spack/licenses/intel/license.lic; s intel-parallel-studio@cluster.2017.2%intel@17.0.2 +openmp+mpi+mkl+ipp 

# CUDA
s cuda@8
s cuda@7
s cuda@6

# Tools
# s git-lfs 	$cc	
s git 		$cc	
s parallel 	$cc	
s emacs 	$cc	
s vim 		$cc	

# MPI Libraries
for compiler in "${compilers[@]}"
do
	for mpi in "${mpis[@]}"
	do
		if [[ $mpi != "intel"* ]]; then
			s $mpi $compiler
		fi
	done
done

# Others
s openmpi@2.0.2 %gcc@5.4.0
