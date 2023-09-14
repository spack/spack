# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypesUrllib3(PythonPackage):
    """Typing stubs for urllib3."""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-urllib3/types-urllib3-1.26.24.tar.gz"

    version("1.26.24", sha256="a1b3aaea7dda3eb1b51699ee723aadd235488e4dc4648e030f09bc429ecff42f")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
