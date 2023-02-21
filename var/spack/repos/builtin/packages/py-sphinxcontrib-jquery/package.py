# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribJquery(PythonPackage):
    """A sphinx extension which ensure that jQuery is installed with Sphinx."""

    homepage = "https://github.com/sphinx-contrib/jquery"
    pypi = "sphinxcontrib-jquery/sphinxcontrib-jquery-2.0.0.tar.gz"

    version("2.0.0", sha256="8fb65f6dba84bf7bcd1aea1f02ab3955ac34611d838bcc95d4983b805b234daa")

    depends_on("python@3.5:", when="@2:", type=("build", "run"))
    depends_on("py-setuptools@65:", type=("build", "run"))
    depends_on("py-flit-core@3.7:", when="@3:", type="build")
