# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTrata(PythonPackage):
    """A Bayesian sampling tool for generating samples 
    and exploring design paramater spaces."""

    homepage = "https://github.com/LLNL/trata"
    pypi = "trata/trata-1.0.1.tar.gz"
    git = "https://github.com/LLNL/trata"

    # notify when the package is updated
    maintainers("sbeljurf", "doutriaux1")

    # git branches
    version("main", branch="main")

    # pypi releases
    version("1.0.1", sha256="98f5179604135c1922839ebaf781c98b60a55a2ad9b9d88e6e9f07fc2f7206f2")

    depends_on("py-setuptools", type=("build"))
    depends_on("py-poetry", type=("build"))

    with when("@3:"):
        depends_on("py-numpy", type=("build", "run"))
        depends_on("py-scipy", type=("build", "run"))
        depends_on("py-scikit-learn", type=("build", "run"))
        depends_on("py-matplotlib", type=("build", "run"))
