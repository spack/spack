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
    gcc@5.4.0
    intel@17.0.4
)

mpis=(
    openmpi@2.1.1~cuda fabrics=pmi,verbs ~java schedulers=slurm
    openmpi@2.1.1+cuda fabrics=pmi,verbs ~java schedulers=slurm
    mpich@3.2+hydra+pmi+romio+verbs
)

mpipkgs=(
    fftw@3.3.6-pl2+mpi+float+long_double+openmp
)

nonmpipkgs=(
    python@2.7.13
    python@3.6.1
    miniconda2@4.3.14
    miniconda3@4.3.14
    openblas@0.2.19+openmp
    r@3.4.0+external-lapack
    boost@1.63.0
    perl@5.24.1
    sga@0.10.15
    boost@1.64.0
    #gromacs@5.1.4+debug+mpi+plumed
    #gromacs@5.1.4+debug+mpi+plumed+cuda
)

# MPI-dependent Libraries
for mpi in "${mpipkgs[@]}"
do
    for compiler in "${compilers[@]}"
    do
        s $mpi %$compiler
        for pkg in "${mpipkgs[@]}"
        do
            s $pkg ^$mpi %$compiler
        done
    done
done

# Non-MPI packages
for compiler in "${compilers[@]}"
do
    for pkg in "${nonmpipkgs[@]}"
    do
        s $pkg %$compiler
    done
done
