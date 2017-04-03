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
    gcc@6.3.0
    intel@17.0.2
)

mpis=(
    openmpi@2.0.2%gcc@6.3.0~java~mxm+pmi~psm~psm2+slurm~sqlite3~thread_multiple~tm+verbs+vt
    openmpi@2.0.2%intel@17.0.2~java~mxm+pmi~psm~psm2+slurm~sqlite3~thread_multiple~tm+verbs+vt 
    mpich@3.2%gcc@6.3.0+hydra+pmi+romio+verbs
    mpich@3.2%intel@17.0.2+hydra+pmi+romio+verbs
    mpich@3.2%pgi@16.10+hydra+pmi+romio+verbs
    mvapich2@2.2%gcc@6.3.0~debug~gforker~hydra~mrail~nemesis~nemesisib+nemesisibtcp~psm~remshell+slurm~sock
    mvapich2@2.2%intel@17.0.2~debug~gforker~hydra~mrail~nemesis~nemesisib+nemesisibtcp~psm~remshell+slurm~sock
    intel-parallel-studio@cluster.2017.2%intel@17.0.2~all+daal~ilp64+ipp+mkl+mpi~newdtags+openmp+rpath+shared+tools
)

mpipkgs=(
  fftw@3.3.6-pl2+mpi
  mdtest
  simul
)

nonmpipkgs=(
  python@2.7.13
  python@3.6.0 
  anaconda2@4.3.0
  anaconda3@4.3.0
  openblas@0.2.19
  r@3.3.2      
  boost@1.63.0
  perl@5.24.1
)

# Non-MPI packages
for compiler in "${compilers[@]}"
do
	for pkg in "${nonmpipkgs[@]}"
	do
		s $pkg %$compiler
	done
done

# MPI-dependent Libraries
for mpi in "${mpis[@]}"
do
	for pkg in "${mpipkgs[@]}"
	do
		s $pkg ^$mpi
	done
done

# Other packages
s sga %intel@17.0.2
s sga %gcc@5.4.0
s gromacs@5.1.2+mpi         %gcc@5.4.0      ^openmpi@2.0.2
s gromacs@5.1.2+mpi         %intel@17.0.2   ^openmpi@2.0.2
s gromacs@5.1.2+mpi         %intel@17.0.2   ^intel-parallel-studio@cluster.2017.2
s gromacs@5.1.2+mpi+cuda    %gcc@5.4.0      ^openmpi@2.0.2
s gromacs@5.1.2+mpi+cuda    %intel@17.0.2   ^openmpi@2.0.2
s gromacs@5.1.2+mpi+cuda    %intel@17.0.2   ^intel-parallel-studio@cluster.2017.2
