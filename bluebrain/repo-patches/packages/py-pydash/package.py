# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydash(PythonPackage):
    """The kitchen sink of Python utility libraries for
    doing stuff in a functional way"""

    homepage = "https://github.com/dgilland/pydash"
    git = "https://github.com/dgilland/pydash.git"
    pypi = "pydash/pydash-5.1.0.tar.gz"

    version("5.1.0", sha256="1b2b050ac1bae049cd07f5920b14fabbe52638f485d9ada1eb115a9eebff6835")

    depends_on("py-typing-extensions@3.10:", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
    depends_on("python@3.7:")
