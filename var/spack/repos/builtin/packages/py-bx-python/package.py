# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBxPython(PythonPackage):
    """The bx-python project is a python library and associated set of scripts
    to allow for rapid implementation of genome scale analyses."""

    homepage = "https://github.com/bxlab/bx-python"
    pypi = "bx-python/bx-python-0.8.8.tar.gz"

    version("0.9.0", sha256="fe545c44d2ea74b239d41e9090618aaf6a859d1a1f64b4a21b133cb602dfdb49")
    version("0.8.8", sha256="ad0808ab19c007e8beebadc31827e0d7560ac0e935f1100fb8cc93607400bb47")

    depends_on("python@3.7:", when="@0.8.13:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-six", when="@:0.8.9", type=("build", "run"))
    # py-python-lzo is listed as a dependency in `tox.ini` rather than in `setup.cfg`
    depends_on("py-python-lzo@1.14:", type=("build", "run"))
