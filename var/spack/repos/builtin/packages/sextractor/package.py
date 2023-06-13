# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------

from spack.package import *


class Sextractor(AutotoolsPackage):
    """SExtractor (Source-Extractor) is a program that builds a catalog of
    objects from an astronomical image. It is particularly oriented towards the
    reduction of large scale galaxy-survey data, but it also performs well on
    moderately crowded star fields."""

    homepage = "https://sextractor.readthedocs.io"
    url = "https://github.com/astromatic/sextractor/archive/refs/tags/2.28.0.tar.gz"
    git = "https://github.com/astromatic/sextractor.git"

    maintainers("rkalescky")

    version("develop")
    version("2.28.0", sha256="36f5afcdfe74cbf1904038a4def0166c1e1dde883e0030b87280dfbdfcd81969")
    version("2.25.0", sha256="ab8ec8fe2d5622a94eb3a20d007e0c54bf2cdc04b8d632667b2e951c02819d8e")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    variant("cfitsio", default=True)

    depends_on("blas")
    depends_on("fftw-api")
    depends_on("cfitsio", when="+cfitsio")

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = []
        spec = self.spec
        blas = spec["blas"].prefix
        mkls = ["mkl", "intel-mkl", "intel-oneapi-mkl", "intel-parallel-studio"]
        if "openblas" in spec:
            args.append("--enable-openblas")
            args.append("--with-openblas-incdir={}".format(blas.include))
            args.append("--with-openblas-libdir={}".format(blas.lib))
        elif any(mkl in spec for mkl in mkls):
            args.append("--enable-mkl")
            args.append("--with-mkl-dir={}".format(blas))
        if spec.satisfies("~cfitsio"):
            args.append("--disable-cfitsio")
        return args

