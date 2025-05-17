# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems import cmake, makefile
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.makefile import MakefilePackage
from spack_repo.builtin.build_systems.python import PythonPipBuilder

from spack.package import *


class Jsonnet(MakefilePackage, CMakePackage):
    """A data templating language for app and tool developers based on JSON"""

    homepage = "https://jsonnet.org/"
    git = "https://github.com/google/jsonnet.git"
    url = "https://github.com/google/jsonnet/archive/refs/tags/v0.18.0.tar.gz"

    maintainers("greenc-FNAL", "gartung", "jcpunk", "marcmengel", "marcpaterno")

    license("Apache-2.0")

    version("master", branch="master")
    version("0.21.0", sha256="a12ebca72e43e7061ffe4ef910e572b95edd7778a543d6bf85f6355bd290300e")
    version("0.20.0", sha256="77bd269073807731f6b11ff8d7c03e9065aafb8e4d038935deb388325e52511b")
    version("0.19.1", sha256="f5a20f2dc98fdebd5d42a45365f52fa59a7e6b174e43970fea4f9718a914e887")
    version("0.18.0", sha256="85c240c4740f0c788c4d49f9c9c0942f5a2d1c2ae58b2c71068107bc80a3ced4")
    version("0.17.0", sha256="076b52edf888c01097010ad4299e3b2e7a72b60a41abbc65af364af1ed3c8dbe")

    variant("python", default=False, description="Provide Python bindings for jsonnet")

    build_system("makefile", conditional("cmake", when="@0.21.0:"), default="makefile")

    conflicts("%gcc@:5.4.99", when="@0.18.0:")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    with when("build_system=cmake"):
        depends_on("nlohmann-json@3.6.1:")

    extends("python", when="+python")
    depends_on("py-setuptools", type=("build",), when="+python")
    depends_on("py-pip", type=("build",), when="+python")
    depends_on("py-wheel", type=("build",), when="+python")


class MakefileBuilder(makefile.MakefileBuilder):

    @property
    def install_targets(self):
        return ["PREFIX={0}".format(self.prefix), "install"]

    @run_after("install")
    def python_install(self):
        if self.pkg.spec.satisfies("+python"):
            pip(*PythonPipBuilder.std_args(self.pkg), f"--prefix={self.pkg.prefix}", ".")


class CMakeBuilder(cmake.CMakeBuilder):

    def cmake_args(self):
        return [
            self.define("USE_SYSTEM_JSON", True),
            self.define("BUILD_SHARED_BINARIES", True),
            self.define("BUILD_TESTS", self.pkg.run_tests),
        ]

    @run_after("install")
    def python_install(self):
        if self.pkg.spec.satisfies("+python"):
            pip(*PythonPipBuilder.std_args(self.pkg), f"--prefix={self.pkg.prefix}", ".")
