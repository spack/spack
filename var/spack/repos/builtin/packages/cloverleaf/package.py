# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class Cloverleaf(MakefilePackage):
    """Proxy Application. CloverLeaf is a miniapp that solves the
    compressible Euler equations on a Cartesian grid,
    using an explicit, second-order accurate method.
    """
    homepage = "https://uk-mac.github.io/CloverLeaf"

    # cuda: done
    version("master_cuda", branch="master",git="https://github.com/UK-MAC/CloverLeaf_CUDA")
    # mpi_only: done
    version("master_mpi_only", branch="master",git="https://github.com/UK-MAC/CloverLeaf_MPI")
    version("1.3_mpi_only", commit="a675f0d63ea72ef386c7c497b08d1e6ca4f89479",git="https://github.com/UK-MAC/CloverLeaf_MPI")
    # openacc_cray: done
    version("master", branch="master",git="https://github.com/UK-MAC/CloverLeaf_OpenACC", when="build=openacc_cray")
    version("1.3", commit="0ddf495cf21cc59f84e274617522a1383e2c328c",git="https://github.com/UK-MAC/CloverLeaf_OpenACC", when="build=openacc_cray")
    version("1.1", commit="5667c3aa565c79cb43b7d956c84c68b6d82d1e94",git="https://github.com/UK-MAC/CloverLeaf_OpenACC", when="build=openacc_cray")
    # openmp_only: done
    version("master", branch="master",git="https://github.com/UK-MAC/CloverLeaf_OpenMP", when="build=openmp_only")
    version("1.3", commit="0fdb917bf10d20363dd8b88d762851908643925b",git="https://github.com/UK-MAC/CloverLeaf_OpenMP", when="build=openmp_only")
    # openmp4_only: done
    version("master", branch="master",git="https://github.com/UK-MAC/CloverLeaf_OpenMP4", when="build=openmp4_only")
    # openmp_offload: done
    version("master", branch="master",git="https://github.com/UK-MAC/CloverLeaf_Offload", when="build=openmp_offload")
    # ref: done
    version("master_ref", branch="master",git="https://github.com/UK-MAC/CloverLeaf_ref")
    version("1.3_ref", commit="0ddf495cf21cc59f84e274617522a1383e2c328c",git="https://github.com/UK-MAC/CloverLeaf_ref")
    version("1.1_ref", commit="5667c3aa565c79cb43b7d956c84c68b6d82d1e94", git="https://github.com/UK-MAC/CloverLeaf_ref")
    # serial: done
    version("master_serial", branch="master",git="https://github.com/UK-MAC/CloverLeaf_Serial")
    version("1.3_serial", commit="b9a2b9c496b5eb1e7e30912d58e32d9dce930a0c",git="https://github.com/UK-MAC/CloverLeaf_Serial")

    variant("ieee", default=False, description="Build with IEEE standards")
    variant("debug", default=False, description="Build with DEBUG flags")

    depends_on("mpi", when="@master_cuda")
    depends_on("mpi", when="@master_mpi_only")
    depends_on("mpi", when="@master_openacc_cray")
    depends_on("mpi", when="@master_ref")
    depends_on("cuda", when="@master_cuda")

    conflicts("@master_cuda", when="%aocc", msg="Currently AOCC supports only ref and MPI variants")
    conflicts("@master_openacc_cray", when="%aocc", msg="Currently AOCC supports only ref and MPI variants")
    conflicts("@master_serial", when="%aocc", msg="Currently AOCC supports only ref and MPI variants")
    conflicts("@master_openmp_only", when="%aocc", msg="Currently AOCC supports only ref and MPI variants")
    conflicts("@master_oenmp4_only", when="%aocc", msg="Currently AOCC supports only ref and MPI variants")
    conflicts("@master_openmp_offload", when="%aocc", msg="Currently AOCC supports only ref and MPI variants")

    @property
    def build_targets(self):
        targets = ["--directory=./"]

        if "mpi" in self.spec:
            targets.append("MPI_COMPILER={0}".format(self.spec["mpi"].mpifc))
            targets.append("C_MPI_COMPILER={0}".format(self.spec["mpi"].mpicc))
        else:
            targets.append("MPI_COMPILER=f90")
            targets.append("C_MPI_COMPILER=cc")

        if "%gcc" in self.spec:
            targets.append("COMPILER=GNU")
#            targets.append("FLAGS_GNU=")
#            targets.append("CFLAGS_GNU=")
        elif "%cce" in self.spec:
            targets.append("COMPILER=CRAY")
            targets.append("FLAGS_CRAY=")
            targets.append("CFLAGS_CRAY=")
        elif "%intel" in self.spec:
            targets.append("COMPILER=INTEL")
        elif "%aocc" in self.spec:
            targets.append("COMPILER=AOCC")
            targets.append("OMP_AOCC=-fopenmp")
            targets.append("FLAGS_AOCC=   -Ofast -fnt-store=aggressive")
            targets.append("CFLAGS_AOCC= -Ofast -fnt-store=aggressive")
        elif "%pgi" in self.spec:
            targets.append("COMPILER=PGI")
            targets.append("FLAGS_PGI=")
            targets.append("CFLAGS_PGI=")
        elif "%xl" in self.spec:
            targets.append("COMPILER=XLF")
            targets.append("FLAGS_XLF=")
            targets.append("CFLAGS_XLF=")

        # Explicit mention of else clause is not working as expected
        # So, not mentioning them
        if "+debug" in self.spec:
            targets.append("DEBUG=1")

        if "%aocc +ieee" in self.spec:
            targets.append("IEEE=1")
            targets.append("OMP_AOCC=-fopenmp")
            targets.append("FLAGS_AOCC=")
            targets.append("CFLAGS_AOCC=")
            targets.append("I3E_AOCC=-O3 -ffp-model=precise")
        
        return targets

    def install(self, spec, prefix):

        mkdirp(prefix.bin)
        mkdirp(prefix.doc.tests)

        install("./clover_leaf", prefix.bin)
        install("./clover.in", prefix.bin)
        install("./*.in", prefix.doc.tests)

