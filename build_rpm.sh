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
for pkg in ["jdk@8u141-b15%gcc@4.8.5",
            # "bazel@0.4.5%gcc@4.8.",
            "maven@3.3.9%gcc@4.8.",
            "gradle@3.4%gcc@4.8.5",
            "ant@1.9.9%gcc@4.8.5",
            "sbt@0.13.12%gcc@4.8.5",
            "cmake@3.11.1%gcc@4.8.5",
            "environment-modules@3.2.10",
            "intel-parallel-studio@cluster.2018.1+advisor+clck+daal+inspector+ipp+itac+mkl+mpi+tbb+vtune  %intel@18.0.1 threads=openmp"]:
          os.system("spack install {}".format(pkg))

# Build non-MPI packages
nonmpipkgs = {"miniconda2@4.3.30": [""],
              "miniconda3@4.3.30": [""],
              "openblas@0.2.20 threads=openmp": [""],
              "perl@5.24.1": [""],
              "sga@0.10.15": [""],
              "boost@1.64.0": [""],
              "cuda@9.1.85": [""],
              "cuda@8.0.61": [""],
              "cuda@7.5.18": [""],
              "cuda@6.5.14": [""],
              "cudnn@7.0": ["^cuda@9.1.85", "^cuda@8.0.61"],
              "cudnn@6.0": ["^cuda@8.0.61"],
              "cudnn@5.1": ["^cuda@8.0.61"],
              "samtools@1.6": [""],
              "glib@2.53.1": [""],
              "bwa@0.7.17": [""],
              "r@3.4.3+external-lapack": ["^openblas threads=openmp", "^intel-parallel-studio+mkl"],
              "octave+qt~readline@4.2.1": ["^openblas threads=openmp"],
              "fftw@3.3.7~mpi+openmp": [""],
              # "fftw@2.1.5~mpi+openmp": [""],
              "eigen~fftw~metis~scotch~suitesparse@3.3.3": [""],
              "opencv+core+eigen+imgproc+openmp+jpeg+png+tiff@3.3.0": ["^eigen~fftw~metis~scotch~suitesparse@3.3.3"],
              "gsl@1.16": [""],
              "gsl@2.4": [""],
              "glib@2.53.1": [""],
              "gmp@6.1.2": [""],
              "ffmpeg@3.2.4": [""],
              "bamtools@2.4.1": [""],
              "bcftools@1.6": [""],
              "hdf5@1.10.1+cxx+fortran+threadsafe~mpi": [""]
}
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
MPIS = {"openmpi@2.0.4+pmi~vt~cuda fabrics={} ~java schedulers=slurm".format(OMPIFAB): "",
        "mvapich2@2.2~cuda fabrics={} process_managers=slurm".format(MVFAB): "",
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
mpipkgs = {"fftw@3.3.7+mpi+openmp": [""],
           "hdf5@1.10.1+cxx+fortran+threadsafe+mpi": [""],
           # "fftw@2.1.5+mpi+openmp": [""],
           "gromacs+mpi~cuda@2016.4": ["^fftw+mpi+openmp@3.3.6-pl2"],
           "gromacs+mpi+cuda@2016.4": ["^fftw+mpi+openmp@3.3.6-pl2 ^cuda@9.1.85", "^fftw+mpi+openmp@3.3.6-pl2 ^cuda@8.0.61"],
           "hpl@2.2": ["^openblas threads=openmp", ""]
           # "scotch+mpi@6.0.4": [""]
}
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
