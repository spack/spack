# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibmetatensorTorch(CMakePackage):
    """TorchScript/C++ bindings to metatensor"""

    homepage = "https://docs.metatensor.org"
    url = "https://github.com/metatensor/metatensor/releases/download/metatensor-torch-v0.7.6/metatensor-torch-cxx-0.7.6.tar.gz"
    git = "https://github.com/metatensor/metatensor.git"

    maintainers("HaoZeke", "luthaf")
    license("BSD-3-Clause", checked_by="HaoZeke")

    version("0.7.6", sha256="8dcc07c86094034facba09ebcc6b52f41847c2413737c8f9c88ae0a2990f8d41")
    version("0.7.5", sha256="24611998e076dd0a782a9792f26b315cc57514013715e8a0aedf2a3a891ba1b4")
    version("0.7.4", sha256="356c412d60a88dfe995976eaad3378ea0e0a858bbca8d43ed299b44c7403fefb")
    version("0.7.3", sha256="ea46e44ba3c7379e1134960851fc6cfd0b0f9de1e7154f60c36f4dfbe59449e3")
    version("0.7.2", sha256="f5474438ff298c643d6265cc3141ff95b1d26498f48a9410b611efb619187cd0")

    generator("ninja")

    depends_on("cmake", type="build")
    depends_on("ninja", type="build")
    depends_on("cxx", type="build")
    depends_on("c", type="build")
    depends_on("libmetatensor@0.1.13:", type="run")
    conflicts("libmetatensor@0.2.0:")
    depends_on("py-torch@2.1.0", type=("build", "link"))

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define("CMAKE_BUILD_TYPE", "Release"),
        ]
        return args
