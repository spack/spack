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
for pkg in ["jdk@8u172-b11%gcc@4.8.5",
            "bazel@0.11.1%gcc@4.8.",
            "maven@3.3.9%gcc@4.8.",
            "gradle@3.4%gcc@4.8.5",
            "ant@1.9.9%gcc@4.8.5",
            "sbt@0.13.12%gcc@4.8.5",
            "cmake@3.11.1%gcc@4.8.5",
            "environment-modules@3.2.10",
            "intel-parallel-studio@cluster.2018.1+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune  %intel@18.0.1 threads=openmp"]:
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
        "mvapich2@2.3rc2~cuda fabrics={} process_managers=slurm".format(MVFAB): "",
        # "mvapich2@2.2+cuda fabrics={} process_managers=slurm".format(MVFAB): "^cuda@9.1.85",
        # "mvapich2@2.2+cuda fabrics={} process_managers=slurm".format(MVFAB): "^cuda@8.0.61",
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
for pkg in ["automake", "autoconf", "bison", "m4", "gperf", "flex", "inputproto", "help2man", "pkg-config", "nasm"]:
    os.system("spack uninstall -y --all {}".format(pkg))
