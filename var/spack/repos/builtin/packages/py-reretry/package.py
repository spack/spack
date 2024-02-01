# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyReretry(PythonPackage):
    """Easy to use retry decorator."""

    homepage = "https://github.com/leshchenko1979/reretry"
    pypi = "reretry/reretry-0.11.1.tar.gz"
    maintainers("charmoniumQ")

    version("0.11.1", sha256="4ae1840ae9e443822bb70543c485bb9c45d1d009e32bd6809f2a9f2839149f5d")

    depends_on("py-setuptools", type="build")
    depends_on("py-pbr", type="build")
