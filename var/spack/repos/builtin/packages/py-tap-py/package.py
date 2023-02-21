# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTapPy(PythonPackage):
    """Python TAP interface module for unit tests"""

    homepage = "https://github.com/python-tap/tappy"
    pypi = "tap.py/tap.py-3.0.tar.gz"

    version("3.0", sha256="f5eeeeebfd64e53d32661752bb4c288589a3babbb96db3f391a4ec29f1359c70")
    version("2.6.2", sha256="5f219d92dbad5e378f8f7549cdfe655b0d5fd2a778f9c83bee51b61c6ca40efb")

    extends("python", ignore="bin/nosetests|bin/pygmentize")

    depends_on("python@3.5:3.7", when="@3.0:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.5:3.7", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
