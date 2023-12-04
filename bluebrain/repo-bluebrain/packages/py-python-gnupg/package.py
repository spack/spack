# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonGnupg(PythonPackage):
    """A Python API for GNU Privacy Guard"""

    homepage = "https://github.com/vsajip/python-gnupg"
    pypi = "python-gnupg/python-gnupg-0.5.1.tar.gz"

    maintainers("tristan0x")

    version("0.5.1", sha256="5674bad4e93876c0b0d3197e314d7f942d39018bf31e2b833f6788a6813c3fb8")

    depends_on("py-wheel@0.29.0:", type=("build"))

    depends_on("py-setuptools", type="build")
