# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.hooks.sbang import sbang_shebang_line
from spack.package import *


class Pdi(CMakePackage):
    """PDI is a library that aims to decouple high-performance simulation codes
    from Input/Output concerns. It offers a declarative application programming
    interface that enables codes to expose the buffers in which they store data
    and to notify PDI of significant steps of the simulation. It supports a
    plugin system to make existing libraries such as HDF5, SIONlib or FTI
    available to codes, potentially mixed in a single execution."""

    homepage = "https://pdi.dev"
    git = "https://github.com/pdidev/pdi.git"
    url = "https://github.com/pdidev/pdi/archive/refs/tags/1.8.0.tar.gz"

    license("BSD-3-Clause")

    maintainers("jbigot")

    version("develop", branch="main", no_cache=True)
    version("1.8.3", sha256="df7200289a2a368ec874140039b417abdfe681b57fb1b9f4c52f924952226020")
    version("1.8.2", sha256="bb4d1654c97f7ff379067adbff339f8b4117c0cf9432f41f1a5cb20a747cac1a")
    version(
        "1.8.1",
        sha256="43f0c0b2bda5515ecf99da7be1600af2c1f669d6c73e3f309275b14940c7e35c",
        deprecated=True,
    )
    version(
        "1.8.0",
        sha256="5d353bfa64f45ee4715b88bd30330030f79f2020cd6bede0ad9b8f9beddadea9",
        deprecated=True,
    )

    variant("benchs", default=False, description="Build benchmarks")
    variant("docs", default=False, description="Build documentation")
    variant("tests", default=False, description="Build tests")
    variant("fortran", default=True, description="Enable Fortran support")
    variant("python", default=True, description="Enable Python support")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build", when="+fortran")

    depends_on("cmake@3.16.3:", type=("build"))
    depends_on("doxygen@1.8.17:", type=("build"), when="+docs")
    depends_on("paraconf@1: +shared", type=("link", "run"))
    depends_on("paraconf +fortran", type=("link", "run"), when="+fortran")
    depends_on("pkgconfig", type=("build"))
    depends_on("python@3.8.2:3", type=("build", "link", "run"), when="+python")
    depends_on(
        "python@3:3.11.9", type=("build", "link", "run"), when="@:1.8.2 +python"
    )  # Needs distutils.
    depends_on("py-pybind11@2.4.3:2", type=("link"), when="+python")
    depends_on(
        "py-setuptools", type=("build", "link"), when="@1.8.3: +python^python@3.12:"
    )  # Needs distutils.
    depends_on("spdlog@1.5:", type=("link"), when="@1.5:")

    root_cmakelists_dir = "pdi"

    def patch(self):
        # Run before build so that the standard Spack sbang install hook can fix
        # up the path to the python binary the zpp scripts requires. We dont use
        # filter_shebang("vendor/zpp-1.0.16/bin/zpp.in") because the template is
        # not yet instantiated and PYTHON_EXECUTABLE is not yet large enough to
        # trigger the replacement via filter_shebang.

        filter_file(
            r"#!@PYTHON_EXECUTABLE@ -B",
            sbang_shebang_line() + "\n#!@PYTHON_EXECUTABLE@ -B",
            "vendor/zpp-1.0.16/bin/zpp.in",
        )

    @staticmethod
    def version_url(version):
        return f"https://github.com/pdidev/pdi/archive/refs/tags/{version}.tar.gz"

    def url_for_version(self, version):
        return Pdi.version_url(version)

    def cmake_args(self):
        return [
            self.define_from_variant("BUILD_BENCHMARKING", "benchs"),
            self.define_from_variant("BUILD_DOCUMENTATION", "docs"),
            self.define_from_variant("BUILD_FORTRAN", "fortran"),
            self.define_from_variant("BUILD_PYTHON", "python"),
            self.define_from_variant("BUILD_TESTING", "tests"),
        ]
