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

externpkgs=(
    bazel@0.4.5%gcc@4.8.5
    gradle@3.4%gcc@4.8.5
    jdk@8u131-b11%gcc@4.8.5
    gradle@3.4%gcc@4.8.5
    cuda@6.5.14%gcc@4.8.5
    cuda@7.5.18%gcc@4.8.5
    cuda@8.0.61%gcc@4.8.5
    cmake@3.8.1%gcc@4.8.5
)

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
    # fftw@3.3.6-pl2+mpi+float+long_double+openmp
    # gromacs@5.1.4+debug+mpi+plumed
    # gromacs@5.1.4+debug+mpi+plumed+cuda
)

nonmpipkgs=(
    python@2.7.13
    python@3.6.1
    miniconda2@4.3.14
    miniconda3@4.3.14
    openblas@0.2.19+openmp
    r@3.4.1+external-lapack ^openblas+openmp
    perl@5.24.1
    sga@0.10.15
    boost@1.64.0
)

trandeps=(
    autoconf
    automake
    bison
    gperf
    flex
    m4
    inputproto
    help2man
    pkg-config
)

# Register external packages
for pkg in "${externpkgs[@]}"
do
    spack install $pkg
done

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

# Remove transit dependency
for pkg in "${trandeps[@]}"
do
    spack uninstall -y --all $pkg
done
