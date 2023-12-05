# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsharp2(AutotoolsPackage):
    """Libsharp2 is a code library for spherical harmonic transforms (SHTs) and
    spin-weighted spherical harmonic transforms, which evolved from the libpsht
    library. Because the upstream repository has no tags or releases, this
    package tracks the versions published together with HEALPix releases."""

    variant("openmp", default=True, description="Build with openmp support")
    variant("mpi", default=True, description="Build with MPI support")
    variant("pic", default=True, description="Generate position-independent code (PIC)")

    homepage = "https://gitlab.mpcdf.mpg.de/mtr/libsharp"
    git = "https://gitlab.mpcdf.mpg.de/mtr/libsharp.git"

    version("3.82.0", sha256="47629f057a2daf06fca3305db1c6950edb9e61bbe2d7ed4d98ff05809da2a127")

    conflicts("libsharp")

    depends_on("autoconf", type="build")
    depends_on("mpi", when="+mpi")

    configure_directory = "src/common_libraries/libsharp"

    def url_for_version(self, version):
        major, minor, patch = version
        return f"https://sourceforge.net/projects/healpix/files/Healpix_{major}.{minor}/healpix_cxx-{major}.{minor}.{patch}.tar.gz/download"

    def configure_args(self):
        args = []
        if "+openmp" not in self.spec:
            args.append("--disable-openmp")
        if "+mpi" not in self.spec:
            args.append("--disable-mpi")
        if "+pic" in self.spec:
            args.append("--enable-pic")
        return args
