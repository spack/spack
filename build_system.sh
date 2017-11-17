#!/usr/bin/env python3

from spack_install import install
import os

CC  = "gcc@4.8.5"
JDK = "jdk@8u141-b15"

# Install intel Compile
for pkg in ["intel-parallel-studio@cluster.2016.4+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %{} threads=openmp".format(CC),
            "intel-parallel-studio@cluster.2017.4+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %{} threads=openmp".format(CC),
            "intel-parallel-studio@cluster.2018.1+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %{} threads=openmp".format(CC)]:
    os.system("rm -f $HOME/spack/etc/spack/licenses/intel/license.lic")
    install(pkg)

# Install JDK
install("{} %{}".format(JDK, CC))

# Install Java packages
for pgk in ["mavene@3.3.9", "gradle@3.4", "ant@1.9.9", "bazel@0.4.5"]:
    install("{} %{} ^{}".format(pgk, CC, JDK))

# Install non-Java packages
packages = {"gcc~binutils@4.9.4": [""],
            "gcc~binutils@5.4.0": [""],
            "gcc~binutils@6.4.0": [""],
            "pgi+nvidia+single@17.10": [""],
            "cmake@3.9.4": [""],
            "environment-modules@3.2.10": [""],
}
for pkg,specs in packages.items():
    for spec in specs:
        for cc in [CC]:
            install("{} %{} {}".format(pkg, cc, spec))
