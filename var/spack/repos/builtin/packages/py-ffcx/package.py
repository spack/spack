# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFfcx(PythonPackage):
    """Next generation FEniCS Form Compiler"""

    homepage = "https://github.com/FEniCS/ffcx"
    git = "https://github.com/FEniCS/ffcx.git"

    version("master", branch="master")

    extends("python")
    depends_on("py-setuptools")
    depends_on("py-cffi")
    depends_on("py-ufl@master")
    depends_on("py-fiat@master")
    depends_on("py-numpy")
