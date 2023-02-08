# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyChemfiles(CMakePackage):
    """Python interface to chemfiles"""

    homepage = "http://chemfiles.org/chemfiles.py/latest/"
    url = "https://github.com/chemfiles/chemfiles.py/archive/refs/tags/0.10.3.tar.gz" 
    maintainers("RMeli")

    version("0.10.3", sha256="0e12837a332e6c1c950e82e339b17cd8fbf29a28bae8399a664b818c056786a9")
    version("0.10.2", sha256="a94e7fb9bae7f0b1658b9b3daab576cf98ea86779ad812abe9e70f49ee0cec48")
    version("0.10.1", sha256="32cee8caa9a626340e3a4b74aa7e50559cf06fae80d052dbb8bd223b47cbee63")
    version("0.10.0", sha256="b4438692d69a0e325157ff0b0ca441ae9b790a2b3104d92cd5b30920cd07fabe")

    extends("python")
    depends_on("chemfiles+shared")

    def cmake_args(self):
        args = ["-DCHFL_PY_INTERNAL_CHEMFILES=OFF"]
        return args
