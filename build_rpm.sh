#!/usr/bin/env python3

from spack_install import install
from spack_install import check_pass
import os, sys

if len(sys.argv) > 1:
          PLATFORM = sys.argv[1]
else:
          PLATFORM = sandybridge

COMPILERS = ["gcc@5.4.0", "intel@18.0.1"]

# Register exernal packages
for pkg in ["jdk@1.8.0_181-b13%gcc@4.8.5",
            "environment-modules@3.2.10%gcc@4.8.5",
            "gcc@6.4.0%gcc@4.8.5",
            "gcc@5.4.0%gcc@4.8.5",
            "gcc@4.9.4%gcc@4.8.5",
            "intel-parallel-studio@cluster.2016.4+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@16.0.4 threads=openmp",
            "intel-parallel-studio@cluster.2017.5+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@17.0.5 threads=openmp",
            "intel-parallel-studio@cluster.2017.7+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@17.0.7 threads=openmp",
            "intel-parallel-studio@cluster.2018.1+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@18.0.1 threads=openmp",
            "intel-parallel-studio@cluster.2018.3+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@18.0.3 threads=openmp"]:
          os.system("spack install {}".format(pkg))

# Build non-MPI packages
nonmpipkgs = {}
for pkg,specs in nonmpipkgs.items():
    for spec in specs:
        for compiler in COMPILERS:
                if check_pass(pkg, compiler, spec, PLATFORM):
                          install("{} %{} {}".format(pkg, compiler, spec))


if os.system("lspci | grep Omni-Path") == 0:
    MVFAB = "psm"
    OMPIFAB = "psm2"
elif os.system("lspci | grep Mellanox") == 0:
    MVFAB = "mrail"
    OMPIFAB = "verbs"
else:
    MVFAB = ""
    OMPIFAB = ""

# Build MPI libraries
MPIS = {"openmpi@3.1.0+pmi~vt~cuda fabrics={} ~java schedulers=slurm".format(OMPIFAB): "",
        "mvapich2@2.3~cuda fabrics={} process_managers=slurm file_systems=lustre".format(MVFAB): "",
        # "mvapich2@2.3+cuda fabrics={} process_managers=slurm file_systems=lustre".format(MVFAB): "^cuda@8.0.61",
        "mpich@3.2.1+pmi+hydra+romio+verbs": "",
        "intel-parallel-studio@cluster.2018.1+mpi": ""
}
for pkg,spec in MPIS.items():
    for compiler in COMPILERS:
        if 'intel-parallel' not in pkg:
                if check_pass(pkg, compiler, spec, PLATFORM):
                          install("{} %{} {}".format(pkg, compiler, spec))

# Build MPI packages
mpipkgs = {}
for pkg,specs in mpipkgs.items():
    for spec in specs:
        for compiler in COMPILERS:
            for mpi in MPIS.keys():
                if spec == "":
                   concrete_spec = "{} %{} ^{}".format(pkg, compiler, mpi)
                else:
                   concrete_spec = "{} %{} {} ^{}".format(pkg, compiler, spec, mpi)
                if check_pass(pkg, compiler, spec, mpi, PLATFORM):
                    install(concrete_spec)

# Remove intermediate dependency
for pkg in ["gperf", "inputproto", "help2man", "nasm"]:
    os.system("spack uninstall -y --all {}".format(pkg))
