# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIterativeStats(PythonPackage):
    """Bacis iterative statistics implementation."""

    pypi = "iterative-stats/iterative-stats-4.0.0.zip"
    git = "https://github.com/IterativeStatistics/BasicIterativeStatistics.git"
    maintainers("frobinou")

    version("main", branch="main")
    version("0.0.4", sha256="6e5194ff5ca11e901157aa2a2a9a15ab9bb22ce55d95596b5b3b703b0ea80e69")

    # main dependencies
    depends_on("python@3.8.0:3.10", type=("build", "run"))
    depends_on("py-poetry-core@1.0.0:", type=("build"))
    depends_on("py-pyyaml@6.0", type=("build", "run"))
    depends_on("py-numpy@1.19:1", type=("build", "run"))

    # dev dependencies
    depends_on("py-pytest@6.2.1:6", type=("test"))
    depends_on("py-autopep8@1.6.0", type=("test"))
    depends_on("openturns@1.19", type=("test"))
    depends_on("py-scipy@1.8", type=("test"))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        pytest = which("pytest")
        pytest()
