# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyChemfiles(PythonPackage):
    """Python interface to chemfiles"""

    homepage = "http://chemfiles.org/chemfiles.py/latest/"
    pypi = "chemfiles/chemfiles-0.10.3.tar.gz"

    maintainers("RMeli")

    version("0.10.3", sha256="4bbb8b116492a57dbf6ddb4c84aad0133cd782e0cc0e53e4b957f2d93e6806ea")
    version("0.10.2", sha256="e277725803715762f9ea787f1ed51dbc2a83a47188ca3bf5d77ddcbc527f55f9")
    version("0.10.1", sha256="6fe35c529c2ded099a59b689270ac0368c6aa33664069c1ccf88eb9fb2686906")
    version("0.10.0", sha256="b52bc19ac7967935a2acc896b1b9738bd904444a1fc09589ed6ada7658a02bf4")

    depends_on("python")
    depends_on("chemfiles+shared")
    depends_on("py-numpy")

    depends_on("py-setuptools", type="build")
    depends_on("py-cmake", type="build")
    depends_on("py-ninja", type="build")
