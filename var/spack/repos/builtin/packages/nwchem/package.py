# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class Nwchem(Package):
    """High-performance computational chemistry software"""

    homepage = "https://nwchemgit.github.io"
    url = "https://github.com/nwchemgit/nwchem/releases/download/v7.2.0-release/nwchem-7.2.0-release.revision-d0d141fd-srconly.2023-03-10.tar.bz2"

    tags = ["ecp", "ecp-apps"]

    version(
        "7.2.0",
        sha256="28ea70947e77886337c84e6fae3bdf88f25f0acfdeaf95e722615779c19f7a7e",
        url="https://github.com/nwchemgit/nwchem/releases/download/v7.2.0-release/nwchem-7.2.0-release.revision-d0d141fd-srconly.2023-03-10.tar.bz2",
    )
    version(
        "7.0.2",
        sha256="9bf913b811b97c8ed51bc5a02bf1c8e18456d0719c0a82b2e71223a596d945a7",
        url="https://github.com/nwchemgit/nwchem/releases/download/v7.0.2-release/nwchem-7.0.2-release.revision-b9985dfa-srconly.2020-10-12.tar.bz2",
    )

    variant("openmp", default=False, description="Enables OpenMP support")
    variant("mpipr", default=False, description="Enables ARMCI with progress rank")
    variant("fftw3", default=False, description="Link against the FFTW library")

    # This patch is for the modification of the build system (e.g. compiler flags) and
    # Fortran syntax to enable the compilation with Fujitsu compilers. The modification
    # will be merged to the next release of NWChem (see https://github.com/nwchemgit/nwchem/issues/347
    # for more detail.
    patch("fj.patch", when="@7.0.2 %fj")
    # This patch is for linking the FFTW library in NWChem.
    # It applys only to the 7.2.0 source code.
    # will be merged to the next release of NWChem (see https://github.com/nwchemgit/nwchem/issues/792
    # for more detail.
    # This patch is the combination of the following commits
    # https://github.com/nwchemgit/nwchem/commit/b4ec4ade1af434bc80470d6874aebf6fdcd12489
    # https://github.com/nwchemgit/nwchem/commit/376f86f96eb982e83f10514e9dcd994564f973b4
    # https://github.com/nwchemgit/nwchem/commit/c89fc9d1eca6689bce12564a63fdea95d962a123
    # Prior versions of NWChem, including 7.0.2, were not able to link with FFTW
    patch("fftw_splans.patch", when="@7.2.0")

    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi")
    depends_on("scalapack")
    depends_on("fftw-api")
    depends_on("python@3:3.9", type=("build", "link", "run"), when="@:7.0.2")
    depends_on("python@3", type=("build", "link", "run"), when="@7.2.0:")

    def install(self, spec, prefix):
        scalapack = spec["scalapack"].libs
        lapack = spec["lapack"].libs
        blas = spec["blas"].libs
        fftw = spec["fftw-api:double,float"].libs
        # see https://nwchemgit.github.io/Compiling-NWChem.html
        args = []
        args.extend(
            [
                "NWCHEM_TOP=%s" % self.stage.source_path,
                # NWCHEM is picky about FC and CC. They should NOT be full path.
                # see https://nwchemgit.github.io/Special_AWCforum/sp/id7524
                "CC=%s" % os.path.basename(spack_cc),
                "FC=%s" % os.path.basename(spack_fc),
                "USE_MPI=y",
                "PYTHONVERSION=%s" % spec["python"].version.up_to(2),
                "BLASOPT=%s" % ((lapack + blas).ld_flags),
                "LAPACK_LIB=%s" % lapack.ld_flags,
                "SCALAPACK_LIB=%s" % scalapack.ld_flags,
                "USE_NOIO=Y",  # skip I/O algorithms
                "MRCC_METHODS=y",  # TCE extra module
                "IPCCSD=y",  # TCE extra module
                "EACCSD=y",  # TCE extra module
                "V=1",  # verbose build
            ]
        )
        if self.spec.satisfies("@7.2.0:"):
            args.extend(["NWCHEM_MODULES=all python gwmol"])
            args.extend(["USE_HWOPT=n"])
        else:
            args.extend(["NWCHEM_MODULES=all python"])
            # archspec flags are injected through the compiler wrapper
            filter_file("(-mtune=native|-mcpu=native|-xHost)", "", "src/config/makefile.h")

        # TODO: query if blas/lapack/scalapack uses 64bit Ints
        # A flag to distinguish between 32bit and 64bit integers in linear
        # algebra (Blas, Lapack, Scalapack)
        use_32_bit_lin_alg = True

        if use_32_bit_lin_alg:
            args.extend(["USE_64TO32=y", "BLAS_SIZE=4", "SCALAPACK_SIZE=4"])
        else:
            args.extend(["BLAS_SIZE=8", "SCALAPACK_SIZE=8"])

        if sys.platform == "darwin":
            target = "MACX64"
            args.extend(["CFLAGS_FORGA=-DMPICH_NO_ATTR_TYPE_TAGS"])
        else:
            target = "LINUX64"

        args.extend(["NWCHEM_TARGET=%s" % target])

        if "+openmp" in spec:
            args.extend(["USE_OPENMP=y"])

        if "+mpipr" in spec:
            args.extend(["ARMCI_NETWORK=MPI-PR"])

        if "+fftw3" in spec:
            args.extend(["USE_FFTW3=y"])
            args.extend(["LIBFFTW3=%s" % fftw.ld_flags])
            args.extend(["FFTW3_INCLUDE={0}".format(spec["fftw-api"].prefix.include)])

        with working_dir("src"):
            make("nwchem_config", *args)
            if use_32_bit_lin_alg:
                make("64_to_32", *args)
            make(*args)

            #  need to install by hand. Follow Ubuntu:
            #  https://packages.ubuntu.com/trusty/all/nwchem-data/filelist
            #  https://packages.ubuntu.com/trusty/amd64/nwchem/filelist
            share_path = join_path(prefix, "share", "nwchem")
            mkdirp(prefix.bin)

            install_tree("data", share_path)
            install_tree(join_path("basis", "libraries"), join_path(share_path, "libraries"))
            install_tree(join_path("basis", "libraries.bse"), join_path(share_path, "libraries"))
            install_tree(join_path("nwpw", "libraryps"), join_path(share_path, "libraryps"))

            b_path = join_path(self.stage.source_path, "bin", target, "nwchem")
            chmod = which("chmod")
            chmod("+x", b_path)
            install(b_path, prefix.bin)

            # Finally, make user's life easier by creating a .nwchemrc file
            # to point to the required data files.
            nwchemrc = """\
   nwchem_basis_library {data}/libraries/
   nwchem_nwpw_library {data}/libraryps/
   ffield amber
   amber_1 {data}/amber_s/
   amber_2 {data}/amber_q/
   amber_3 {data}/amber_x/
   amber_4 {data}/amber_u/
   spce    {data}/solvents/spce.rst
   charmm_s {data}/charmm_s/
   charmm_x {data}/charmm_x/
""".format(
                data=share_path
            )
            with open(".nwchemrc", "w") as f:
                f.write(nwchemrc)
            install(".nwchemrc", share_path)

    def setup_run_environment(self, env):
        env.set("NWCHEM_BASIS_LIBRARY", join_path(self.prefix, "share/nwchem/libraries/"))
        env.set("NWCHEM_NWPW_LIBRARY", join_path(self.prefix, "share/nwchem/libraryps/"))
