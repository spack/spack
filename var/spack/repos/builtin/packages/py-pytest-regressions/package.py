# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestRegressions(PythonPackage):
    """Easy to use fixtures to write regression tests."""

    homepage = "https://github.com/ESSS/pytest-regressions"
    pypi = "pytest-regressions/pytest-regressions-2.3.1.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]

    version("2.3.1", sha256="b3ec4cdb34e8f627606275d8b834c65e60e1a3073e326bb3727a427273d0221d")

    depends_on("py-setuptools", type="build")
    depends_on("py-pytest@3.5:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"))
