# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBlosc(PythonPackage):
    """A Python wrapper for the extremely fast Blosc compression library"""

    homepage = "http://python-blosc.blosc.org"
    url = "https://github.com/Blosc/python-blosc/archive/v1.9.1.tar.gz"
    git = "https://github.com/Blosc/python-blosc.git"

    license("BSD-3-Clause")

    version("1.11.2", sha256="8a0eb2daabb23415c3be3b9473176c75fa150cdb91b2ef42a77f492dad92cb2a")
    version("1.9.1", sha256="ffc884439a12409aa4e8945e21dc920d6bc21807357c51d24c7f0a27ae4f79b9")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python@3.7:", type=("build", "run"), when="@1.9:1.10")
    depends_on("python@3.9:", type=("build", "run"), when="@1.11.2:")

    depends_on("py-setuptools", type="build")
    depends_on("py-scikit-build", type="build")
    depends_on("py-scikit-build@0.11.1:", type="build", when="@1.11.2:")
    depends_on("py-py-cpuinfo", type="build", when="@1.11.2:")
    depends_on("py-versioneer", type="build", when="@1.11.2:")
    depends_on("cmake@3.11:", type="build")
    depends_on("cmake@3.14:", type="build", when="@1.11.2:")
    depends_on("ninja", type="build")

    depends_on("py-numpy@1.16:", type=("build", "run"), when="@1.11.2:")

    # c-blosc is internally vendored but 1.11.2 doesn't correctly ship the
    # c-blosc in the tarball https://github.com/Blosc/python-blosc/issues/337
    # so use the exact c-blosc version as specified in
    # https://github.com/Blosc/python-blosc/releases/tag/v1.11.2
    depends_on("c-blosc@1.21.6", type=("build", "run"), when="@1.11.2 ^python@3.12:")

    def setup_build_environment(self, env):
        if self.spec.satisfies("^c-blosc"):
            env.set("USE_SYSTEM_BLOSC", 1)
