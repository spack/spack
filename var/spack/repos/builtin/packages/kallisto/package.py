# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kallisto(CMakePackage):
    """kallisto is a program for quantifying abundances of transcripts from
    RNA-Seq data."""

    homepage = "https://pachterlab.github.io/kallisto"
    url = "https://github.com/pachterlab/kallisto/archive/v0.43.1.tar.gz"

    version("0.48.0", sha256="1797ac4d1f0771e3f1f25dd7972bded735fcb43f853cf52184d3d9353a6269b0")
    version("0.46.2", sha256="c447ca8ddc40fcbd7d877d7c868bc8b72807aa8823a8a8d659e19bdd515baaf2")
    version("0.43.1", sha256="7baef1b3b67bcf81dc7c604db2ef30f5520b48d532bf28ec26331cb60ce69400")

    # HDF5 support is optional beginning with version 0.46.2.
    variant("hdf5", when="@0.46.2:", default=False, description="Build with HDF5 support")

    depends_on("zlib-api")
    depends_on("hdf5", when="@:0.43")
    depends_on("hdf5", when="+hdf5")

    # htslib isn't built in time to be used....
    parallel = False

    # v0.44.0 vendored a copy of htslib and uses auto* to build
    # its configure script.
    depends_on("autoconf", type="build", when="@0.44.0:")
    depends_on("automake", type="build", when="@0.44.0:")
    depends_on("libtool", type="build", when="@0.44.0:")
    depends_on("m4", type="build", when="@0.44.0:")

    patch("link_zlib.patch", when="@:0.43")
    patch("limits.patch", when="@:0.46")
    patch("htslib_configure.patch", when="@0.44.0:^autoconf@2.70:")

    @run_before("cmake")
    def autoreconf(self):
        # Versions of autoconf greater than 2.69 need config.guess and
        # config.sub in the tree.
        if self.spec.satisfies("@0.44.0:^autoconf@2.70:"):
            with working_dir(join_path(self.stage.source_path, "ext", "htslib")):
                autoreconf = which("autoreconf")
                autoreconf("--install")

    # Including '-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON' in the cmake args
    # causes bits of cmake's output to end up in the autoconf-generated
    # configure script.
    # See https://github.com/spack/spack/issues/15274 and
    # https://github.com/pachterlab/kallisto/issues/253
    @property
    def std_cmake_args(self):
        """Call the original std_cmake_args and then filter the verbose
        setting.
        """
        a = super().std_cmake_args
        if self.spec.satisfies("@0.44.0:"):
            args = [i for i in a if i != "-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON"]
            if self.spec.satisfies("@0.46.2:"):
                args.append(self.define_from_variant("USE_HDF5", "hdf5"))
        else:
            args = a

        return args
