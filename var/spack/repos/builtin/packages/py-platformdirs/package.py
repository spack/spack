# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.build_systems.python
from spack.package import *


class PyPlatformdirs(PythonPackage):
    """A small Python module for determining appropriate
    platform-specific dirs, e.g. a "user data dir" """

    homepage = "https://github.com/platformdirs/platformdirs"
    pypi = "platformdirs/platformdirs-2.4.0.tar.gz"

    version("2.5.2", sha256="58c8abb07dcb441e6ee4b11d8df0ac856038f944ab98b7be6b27b2a3c7feef19")
    version("2.4.1", sha256="440633ddfebcc36264232365d7840a970e75e1018d15b4327d11f91909045fda")
    version("2.4.0", sha256="367a5e80b3d04d2428ffa76d33f124cf11e8fff2acdaa9b43d545f5c7d661ef2")
    version("2.3.0", sha256="15b056538719b1c94bdaccb29e5f81879c7f7f0f4a153f46086d155dffcd4f0f")

    variant(
        "wheel",
        default=False,
        sticky=True,
        description="Install from wheel (required for bootstrapping Spack)",
    )

    depends_on("python@3.7:", when="@2.4.1:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@44:", when="@:2.5.1", type="build")
    depends_on("py-setuptools-scm@5:+toml", when="@:2.5.1", type="build")
    depends_on("py-hatchling@0.22.0:", when="@2.5.2:", type="build")
    depends_on("py-hatch-vcs", when="@2.5.2:", type="build")


class PythonPipBuilder(spack.build_systems.python.PythonPipBuilder):
    @when("+wheel")
    def install(self, pkg, spec, prefix):
        args = list(filter(lambda x: x != "--no-index", self.std_args(self.pkg)))
        args += [f"--prefix={prefix}", self.spec.format("platformdirs=={version}")]
        pip(*args)
