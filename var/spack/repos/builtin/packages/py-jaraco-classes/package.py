# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJaracoClasses(PythonPackage):
    """Utility functions for Python class constructs"""

    homepage = "https://github.com/jaraco/jaraco.classes"
    pypi = "jaraco.classes/jaraco.classes-3.2.2.tar.gz"

    version("3.2.2", sha256="6745f113b0b588239ceb49532aa09c3ebb947433ce311ef2f8e3ad64ebb74594")

    depends_on("python@3.7:", type=("build", "run"))

    depends_on("py-setuptools@56:", type="build")
    depends_on("py-setuptools-scm@3.4.1: +toml", type="build")

    depends_on("py-more-itertools", type=("build", "run"))
