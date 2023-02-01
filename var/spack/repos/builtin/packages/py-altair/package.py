# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAltair(PythonPackage):
    """Declarative statistical visualization library for Python"""

    pypi = "altair/altair-4.2.0.tar.gz"

    version("4.2.0", sha256="d87d9372e63b48cd96b2a6415f0cf9457f50162ab79dc7a31cd7e024dd840026")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@40.6:", type="build")
    depends_on("py-entrypoints", type=("build", "run"))
    depends_on("py-jsonschema@3:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas@0.18:", type=("build", "run"))
    depends_on("py-toolz", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
