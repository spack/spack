# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygithub(PythonPackage):
    """Use the full Github API v3"""

    homepage = "https://pygithub.readthedocs.io/"
    pypi = "PyGithub/PyGithub-1.54.1.tar.gz"

    version("1.55", sha256="1bbfff9372047ff3f21d5cd8e07720f3dbfdaf6462fcaed9d815f528f1ba7283")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-deprecated", type=("build", "run"))
    depends_on("py-pyjwt@2:", type=("build", "run"))
    depends_on("py-pynacl@1.4.0:", type=("build", "run"))
    depends_on("py-requests@2.14.0:", type=("build", "run"))
