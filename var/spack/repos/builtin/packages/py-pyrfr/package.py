# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyrfr(PythonPackage):
    """This package serves as the python interface to RFR, an
    extensible C++ librarry for random forests."""

    homepage = "https://automl.github.io/random_forest_run/installation.html"
    pypi = "pyrfr/pyrfr-0.8.2.tar.gz"

    version("0.8.2", sha256="c18a6e8f0bd971c1ea449b6dd0997a6ec1fe9a031883400bdcc95fa5ddd65975")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("swig")
