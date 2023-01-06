# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class PyLagom(PythonPackage):
    """Lagom is a dependency injection container
    designed to give you 'just enough' help with building your dependencies.
    """

    homepage = "https://lagom-di.readthedocs.io"
    url = "https://github.com/meadsteve/lagom/archive/refs/tags/2.0.0.tar.gz"
    git = "https://github.com/meadsteve/lagom.git"

    version("2.2.0", sha256="ab7fc2b63ef65e3f8cbaec67d165d8992f8addc23d42f2bc395f1db5eef1a5aa")

    depends_on("py-setuptools", type="build")
