# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySlepc4py(PythonPackage):
    """This package provides Python bindings for the SLEPc package."""

    homepage = "https://gitlab.com/slepc/slepc4py"
    url = "https://slepc.upv.es/download/distrib/slepc4py-3.17.1.tar.gz"
    git = "https://gitlab.com/slepc/slepc.git"

    maintainers("joseeroman", "balay")

    version("main", branch="main")
    version("3.18.2", sha256="402297fd8e583ed2618d2cba05e5cae8e9d0a2c3943812a1a138f431ef3479b3")
    version("3.18.1", sha256="4c2bc0947d6a9cdb209e3174b7f54fe7b029220e2c90106f52844e8f8795f8f0")
    version("3.18.0", sha256="aa83f46f942aca05ffcbc8be29b496f56837f564e0396f5b39cec4946654ee78")
    version("3.17.2", sha256="e5b235486b6901cd4ff0d94083f0e5eeacaef3a2893e1714769717ad488a3885")
    version("3.17.1", sha256="967d5d045526088ff5b7b2cde76f8b4d1fee3a2a68481f85224b0795e6613eb9")
    version("3.17.0", sha256="cab298eb794739579167fd60ff900db90476c4c93b4ae4e0204e989a6eeb3767")
    version("3.16.3", sha256="d97652efe60163d30c24eb1ef1b1ba98bb8239fd7452bdf8207c2505da48d77e")
    version("3.16.2", sha256="a3950b2d4876e8b7429cf5b7d0faed580a70bbd17735b0279aeda460a4a32e18")
    version("3.16.1", sha256="3ce93de975fa3966794efb09c315b6aff17e412197f99edb66bbfa71fc49093b")
    version("3.16.0", sha256="e18850ebccb1e7c59accfbdbe4d004402abbde7f4e1291b0d2c5b560b308fb88")
    version("3.15.2", sha256="c87135989c4d95b9c92a5b615a95eddc34b69dad9cc28b27d3cb7dfaec46177b")
    version("3.15.1", sha256="bcdab6d2101ae00e189f4b33072805358cee2dda806a6b6a8e3c2f1b9f619dfd")
    version("3.15.0", sha256="2f5f5cc25ab4dd3782046c65e97265b39be0cf9cc74c5c0100c3c580c3c32395")
    version("3.13.0", sha256="780eff0eea1a5217642d23cd563786ef22df27e1d772a1b0bb4ccc5701df5ea5")
    version("3.12.0", sha256="d8c06953b7d00f529a9a7fd016dfa8efdf1d05995baeea7688d1d59611f424f7")
    version("3.11.0", sha256="1e591056beee209f585cd781e5fe88174cd2a61215716a71d9eaaf9411b6a775")

    patch("ldshared.patch", when="@:99")
    patch("ldshared-dev.patch", when="@main")

    depends_on("py-cython@0.24:", type="build", when="@main")
    depends_on("py-setuptools", type="build")

    depends_on("py-petsc4py", type=("build", "run"))
    depends_on("py-petsc4py@3.18.0:3.18", when="@3.18.0:3.18", type=("build", "run"))
    depends_on("py-petsc4py@3.17.0:3.17", when="@3.17.0:3.17", type=("build", "run"))
    depends_on("py-petsc4py@3.16.0:3.16", when="@3.16.0:3.16", type=("build", "run"))
    depends_on("py-petsc4py@3.15.0:3.15", when="@3.15.0:3.15", type=("build", "run"))
    depends_on("py-petsc4py@3.13.0:3.13", when="@3.13.0:3.13", type=("build", "run"))
    depends_on("py-petsc4py@3.12.0:3.12", when="@3.12.0:3.12", type=("build", "run"))
    depends_on("py-petsc4py@3.11.0:3.11", when="@3.11.0:3.11", type=("build", "run"))

    depends_on("slepc")
    depends_on("slepc@3.18.0:3.18", when="@3.18.0:3.18")
    depends_on("slepc@3.17.0:3.17", when="@3.17.0:3.17")
    depends_on("slepc@3.16.0:3.16", when="@3.16.0:3.16")
    depends_on("slepc@3.15.0:3.15", when="@3.15.0:3.15")
    depends_on("slepc@3.13.0:3.13", when="@3.13.0:3.13")
    depends_on("slepc@3.12.0:3.12", when="@3.12.0:3.12")
    depends_on("slepc@3.11.0:3.11", when="@3.11.0:3.11")

    @property
    def build_directory(self):
        import os

        if self.spec.satisfies("@main"):
            return os.path.join(self.stage.source_path, "src", "binding", "slepc4py")
        else:
            return self.stage.source_path
