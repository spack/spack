# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPropcache(PythonPackage):
    """Fast property caching"""

    homepage = "https://github.com/aio-libs/propcache"
    pypi = "propcache/propcache-0.3.1.tar.gz"

    license("Apache-2.0")

    version("0.3.1", sha256="40d980c33765359098837527e18eddefc9a24cea5b45e078a7f3bb5b032c6ecf")

    depends_on("py-setuptools@47:", type="build")
    depends_on("py-expandvars", type="build")
    depends_on("py-tomli", when="^python@:3.10", type="build")
    depends_on("py-cython", type="build")

    depends_on("python@3.9:", when="@0.2.1:", type=("build", "run"))
