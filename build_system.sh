#!/usr/bin/env python3

from spack_install import install
import os

CC  = "gcc@4.8.5"
JDK = "jdk@1.8.0_181-b13"

# Install Intel Compiler
for pkg in ["intel-parallel-studio@cluster.2016.4+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %{} threads=openmp".format(CC),
            "intel-parallel-studio@cluster.2017.7+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %{} threads=openmp".format(CC),
            "intel-parallel-studio@cluster.2018.3+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %{} threads=openmp".format(CC)]:
    os.system("rm -f $HOME/spack/etc/spack/licenses/intel/license.lic")
    install(pkg)

# Install Intel Parallel Studio
for pkg in ["intel-parallel-studio@cluster.2016.4+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@16.0.4 threads=openmp",
            "intel-parallel-studio@cluster.2017.7+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@17.0.7 threads=openmp",
            "intel-parallel-studio@cluster.2018.3+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune %intel@18.0.3 threads=openmp"]:
    os.system("rm -f $HOME/spack/etc/spack/licenses/intel/license.lic")
    install(pkg)

# Install JDK
install("{} %{}".format(JDK, CC))

# Install Java packages
for pgk in ["maven@3.3.9", "gradle@4.8.1", "ant@1.9.9", "sbt@1.1.6"]:
    install("{} %{} ^{}".format(pgk, CC, JDK))

# Install non-Java packages
packages = {"miniconda2@4.5.4": [""],
            "miniconda3@4.5.4": [""],
            "gcc~binutils@4.9.4": [""],
            "gcc~binutils@5.4.0": [""],
            "gcc~binutils@6.4.0": [""],
            "gcc~binutils@7.3.0": [""],
            "pgi+nvidia+single~network@18.4": [""],
            "cuda@9.0.176": [""],
            "cuda@8.0.61": [""],
            "cuda@7.5.18": [""],
            "cuda@6.5.14": [""],
            "cudnn@7.0": ["^cuda@9.0.176", "^cuda@8.0.61"],
            "cudnn@6.0": ["^cuda@8.0.61"],
            "cudnn@5.1": ["^cuda@8.0.61"],
            "cmake@3.9.6": [""]
}
for pkg,specs in packages.items():
    for spec in specs:
        for cc in [CC]:
            install("{} %{} {}".format(pkg, cc, spec))

# Remove intermediate dependency
for pkg in ["perl"]:
    os.system("spack uninstall -y {}".format(pkg))
