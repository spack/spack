# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bgen(WafPackage):
    """This repository contains a reference implementation of the BGEN format, written
    in C++. The library can be used as the basis for BGEN support in other software,
    or as a reference for developers writing their own implementations of the BGEN format.

    If you make use of the BGEN library, its tools or example programs, please cite:

    Band, G. and Marchini, J., "BGEN: a binary file format for imputed genotype and
    haplotype data", bioArxiv 308296; doi: https://doi.org/10.1101/308296."""

    homepage = "https://enkre.net/cgi-bin/code/bgen"

    license("BSL-1.0")
    maintainers("teaguesterling")

    version(
        "1.1.7",
        sha256="121f5956f04ad174bc410fa7deed59e2ebff0ec818a3c66cf5d667357dddfb62",
        url="https://enkre.net/cgi-bin/code/bgen/tarball/6ac2d582f9/BGEN-6ac2d582f9.tar.gz",
    )

    variant("source", default=False, description="Install source tree as well")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fossil", type="build")

    def flag_handler(self, name, flags):
        # Version 1.1.7 not compatible with C++17
        if name == "cxxflags":
            flags.append("-std=c++11")
        return (flags, None, None)

    def install(self, spec, prefix):
        super().install(spec, prefix)
        if spec.satisfies("+source"):
            src_dir = join_path(prefix.src.bgen)
            makedirs(src_dir)
            install_tree(self.stage.source_path, src_dir)
