# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.autotools import AutotoolsBuilder, AutotoolsPackage
from spack_repo.builtin.build_systems.cmake import CMakeBuilder, CMakePackage

from spack.package import *


class Libcerf(AutotoolsPackage, CMakePackage):
    """A self-contained C library providing complex error functions, based
    on Faddeeva's plasma dispersion function w(z). Also provides Dawson's
    integral and Voigt's convolution of a Gaussian and a Lorentzian"""

    homepage = "https://jugit.fz-juelich.de/mlz/libcerf/"
    url = "https://jugit.fz-juelich.de/mlz/libcerf/-/archive/v2.4/libcerf-v2.4.tar.gz"

    license("MIT")

    maintainers("white238")

    version("2.4", sha256="080b30ae564c3dabe3b89264522adaf5647ec754021572bee54929697b276cdc")
    version("2.3", sha256="cceefee46e84ce88d075103390b4f9d04c34e4bc3b96d733292c36836d4f7065")
    version(
        "1.3",
        sha256="d7059e923d3f370c89fb4d19ed4f827d381bc3f0e36da5595a04aeaaf3e6a859",
        url="https://sourceforge.net/projects/libcerf/files/libcerf-1.3.tgz",
    )

    variant("cpp", default=False, when="@2:", description="Compile source as C++")

    # Build system
    build_system(
        conditional("cmake", when="@2:"), conditional("autotools", when="@=1.3"), default="cmake"
    )

    depends_on("c", type="build")
    depends_on("fortran", type="build")


class CMakeBuilder(CMakeBuilder):
    def cmake_args(self):
        args = []

        args.append(self.define_from_variant("CERF_CPP", "cpp"))

        return args


class AutotoolsBuilder(AutotoolsBuilder):
    def configure_args(self):
        spec = self.spec
        options = []
        # Clang reports unused functions as errors, see
        # http://clang.debian.net/status.php?version=3.8.1&key=UNUSED_FUNCTION
        if spec.satisfies("%clang") or spec.satisfies("%apple-clang"):
            options.append("CFLAGS=-Wno-unused-function")
        # fujitsu compiler has a error about unused functions too.
        if spec.satisfies("%fj"):
            options.append("CFLAGS=-Wno-unused-function")

        return options
