# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyChemfiles(CMakePackage):
    """Python interface to chemfiles"""

    homepage = "http://chemfiles.org/chemfiles.py/latest/"
    url = "https://files.pythonhosted.org/packages/40/ed/ad8fc9ac327b791bc20a8daf2b1ce3e83b45bed640575b6ac04ec02723ce/chemfiles-0.10.3.tar.gz"

    maintainers("RMeli", "github_user2")

    version("0.10.3", sha256="4bbb8b116492a57dbf6ddb4c84aad0133cd782e0cc0e53e4b957f2d93e6806ea")

    extends("python")
    depends_on("chemfiles+shared")

    def cmake_args(self):
        args = ["-DCHFL_PY_INTERNAL_CHEMFILES=OFF"]
        return args
