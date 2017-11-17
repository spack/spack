#!/usr/bin/env python3

from spack_install import install
import os

COMPILERS = ["gcc@5.4.0", "intel@17.0.5"]

# Register exernal packages
for pkg in ["jdk@8u141-b15%gcc@4.8.5",
            # "bazel@0.4.5%gcc@4.8.",
            "maven@3.3.9%gcc@4.8.",
            "gradle@3.4%gcc@4.8.5",
            "ant@1.9.9%gcc@4.8.5",
            "sbt@0.13.12%gcc@4.8.5",
            "cmake@3.9.4%gcc@4.8.5",
            "environment-modules@3.2.10"]:
          os.system("spack install {}".format(pkg))

# Build non-MPI packages
nonmpipkgs = {"python@2.7.14": [""],
              "python@3.6.2": [""],
              "miniconda2@4.3.30": [""],
              "miniconda3@4.3.30": [""],
              "openblas@0.2.20 threads=openmp": [""],
              "perl@5.24.1": [""],
              "sga@0.10.15": [""],
              "boost@1.64.0": [""],
              "cuda@9.0.176": [""],
              "cuda@8.0.61": [""],
              "cuda@7.5.18": [""],
              "cuda@6.5.14": [""],
              "cudnn@7.0": ["^cuda@9.0.176", "^cuda@8.0.61"],
              "cudnn@6.0": ["^cuda@8.0.61"],
              "cudnn@5.1": ["^cuda@8.0.61"],
              "samtools@1.6": [""],
              "r@3.4.1+external-lapack": ["^openblas threads=openmp", "^intel-parallel-studio+mkl"],
              "fftw@3.3.6-pl2~mpi+openmp": [""]
}
for pkg,specs in nonmpipkgs:
    for spec in specs:
        for compiler in COMPILERS:
            install("{} %{} {}".format(pgk, compiler, spec))


# Build MPI libraries
MPIS = ["openmpi@2.1.2~cuda fabrics=verbs ~java schedulers=slurm",
       "openmpi@2.1.2+cuda fabrics=verbs ~java schedulers=slurm",
       "mvapich2@2.2~cuda fabrics=mrail process_managers=slurm",
       "mvapich2@2.2+cuda fabrics=mrail process_managers=slurm",
       "mpich@3.2+hydra+pmi+romio+verbs"
]
for pkg in MPIS:
    for compiler in COMPILERS:
        install("{} %{}".format(pkg, compiler))

# Build MPI packages
mpipkgs = {["fftw@3.3.6-pl2+mpi+openmp"]: [""],
    ["gromacs+mpi~cuda@5.1.4"]: ["^fftw+mpi+openmp@3.3.6-pl2"],
    ["gromacs+mpi+cuda@5.1.4"]: ["^fftw+mpi+openmp@3.3.6-pl2"]
}
for pkg,specs in mpipkgs.items():
    for spec in specs:
        for compiler in COMPILERS:
            for mpi in MPIS:
                if spec == "":
                   concrete_spec = "{} %{} ^{}".format(pkg, compiler, mpi)
                else:
                   concrete_spec = "{} %{} ^{} {}".format(pkg, compiler, mpi, spec)
                install(concrete_spec) if pass_check(concrete_spec)

# Remove intermediate dependency
for pkg in ["automake", "autoconf", "bison", "m4", "gperf", "flex", "inputproto", "help2man", "pkg-conf", "gdbm", "readline"]:
    os.system("spack uninstall -y --all {}".format(pkg))
