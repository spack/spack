# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Plink2(MakefilePackage):
    """PLINK2: Whole genome association analysis toolset, designed to perform a
    range of basic, large-scale analyses in a computationally efficient manner."""

    homepage = "https://www.cog-genomics.org/plink/2.0/"
    git = "https://github.com/chrchang/plink-ng.git"

    version("2.00a4.3", tag="v2.00a4.3", commit="59fca48f6f8135886ff68962fbe31ae0c6413228")

    depends_on("zlib-api")
    depends_on("zlib@1.2.12:", when="^[virtuals=zlib-api] zlib")
    depends_on("zstd@1.5.2:")
    depends_on("libdeflate@1.10:")
    depends_on("blas")
    depends_on("lapack")

    build_directory = "2.0/build_dynamic"

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            makefile = FileFilter("Makefile")
            if "avx2" in spec.target:
                makefile.filter(r"^NO_AVX2 = 1", "NO_AVX2 =")
            elif "sse4_2" in spec.target:
                makefile.filter(r"^NO_SSE42 = 1", "NO_SSE42 =")
            makefile.filter(r"^STATIC_ZSTD = 1", "STATIC_ZSTD =")
            makefile.filter(
                r"^  BLASFLAGS=-llapack -lblas -lcblas -latlas",
                "  BLASFLAGS={0} {1}".format(
                    spec["blas"].libs.ld_flags, spec["lapack"].libs.ld_flags
                ),
            )

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make()

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        with working_dir(self.build_directory):
            install("plink2", prefix.bin)
            install("pgen_compress", prefix.bin)
