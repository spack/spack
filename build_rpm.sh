#!/bin/bash

function s {
    spack find $@ | grep 'No package'
    if [ $? -eq 0 ]
    then
        spack install --restage $@
    else
        echo "$@ has been installed."
    fi
}

externpkgs=(
    jdk@8u141-b15%gcc@4.8.5
    bazel@0.4.5%gcc@4.8.5
    gradle@3.4%gcc@4.8.5
    ant@1.9.9%gcc@4.8.5
    sbt@0.13.12%gcc@4.8.5
    cmake@3.8.1%gcc@4.8.5
)

compilers=(
    gcc@5.4.0
    intel@17.0.4
)

mpis=(
    'openmpi@2.1.2~cuda fabrics=verbs ~java schedulers=slurm'
    'openmpi@2.1.2+cuda fabrics=verbs ~java schedulers=slurm'
    'mvapich2@2.2~cuda fabrics=mrail process_managers=slurm'
    # 'mvapich2@2.2+cuda fabrics=mrail process_managers=slurm'
    'mpich@3.2+hydra+pmi+romio+verbs'
)

declare -A nonmpipkgs
nonmpipkgs=(
    ["python@2.7.14"]=""
    ["python@3.6.2"]=""
    ["miniconda2@4.3.30"]=""
    ["miniconda3@4.3.30"]=""
    ["openblas@0.2.20 threads=openmp"]=""
    ["perl@5.24.1"]=""
    ["sga@0.10.15"]=""
    ["boost@1.64.0"]=""
    ["cuda@9.0.176"]=""
    ["cuda@8.0.61"]=""
    ["cuda@7.5.18"]=""
    ["cuda@6.5.14"]=""
    ["cudnn@7.0.cuda9"]="^cuda@9.0.176"
    ["cudnn@7.0.cuda8"]="^cuda@8.0.61"
    ["cudnn@6.0.cuda8"]="^cuda@8.0.61"
    ["cudnn@5.1.cuda8"]="^cuda@8.0.61"
    ["samtools@1.6"]=""
    ["r@3.4.1+external-lapack"]="^openblas threads=openmp"
    ["r@3.4.1+external-lapack"]="^intel-parallel-studio+mkl"
    ["fftw@3.3.6-pl2~mpi+openmp"]=""
)

declare -A mpipkgs
mpipkgs=(
    # ["fftw@3.3.6-pl2+mpi+openmp"]=""
    # ["gromacs+mpi~cuda@5.1.4"]="^fftw+mpi+openmp@3.3.6-pl2"
    # ["gromacs+mpi+cuda@5.1.4"]="^fftw+mpi+openmp@3.3.6-pl2"
)

declare -A otherpkgs
otherpkgs=(
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

# Non-MPI packages
for compiler in "${compilers[@]}"
do
    for pkg in "${!nonmpipkgs[@]}"
    do
        s $pkg %$compiler ${nonmpipkgs[$pkg]}
    done
done

# MPI-dependent Libraries
for mpi in "${mpis[@]}"
do
    for compiler in "${compilers[@]}"
    do
        s $mpi %$compiler
        for pkg in "${!mpipkgs[@]}"
        do
            pkgname=$pkg
            pkgspec=${mpipkgs[$pkg]}
            # Rule checking
            if [[ "$mpi" != *"cuda"* ]] && [[ "$pkgname" != *"cuda"* ]]; then
                echo "Build $pkgname^$pkgspec^$mpi against $compiler since CUDA is not involved."
           			s $pkgname %$compiler $pkgspec^$mpi
            elif [[ "$mpi" == "*openmpi*" ]] && [[ "$mpi" == "*+cuda*" ]] && [[ "$pkgname" == "*~cuda*" ]]; then
                continue
            elif [[ "$mpi" == "*openmpi*" ]] && [[ "$mpi" == "*~cuda*" ]] && [[ "$pkgname" == "*+cuda*" ]]; then
                continue
            elif [[ "$mpi" == "*mvapich*" ]] && [[ "$mpi" == "*+cuda*" ]] && [[ "$pkgname" == "*~cuda*" ]]; then
                continue
            elif [[ "$mpi" == "*mvapich*" ]] && [[ "$mpi" == "*~cuda*" ]] && [[ "$pkgname" == "*+cuda*" ]]; then
                continue
            else
                s $pkgname %$compiler $pkgspec^$mpi
            fi
        done
    done
done

# Other packages
for pkg in "${otherpkgs[@]}"
do
    s $pkg
done

# Remove transit dependency
for pkg in "${trandeps[@]}"
do
    spack uninstall -y --all $pkg 2>&1 > /dev/null
done
