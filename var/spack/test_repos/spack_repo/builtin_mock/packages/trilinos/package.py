# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Trilinos(Package):
    """A package which has pure build dependencies, run dependencies, and link dependencies."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/trilinos-1.0.tar.gz"

    version("16.1.0", md5="00000000000000000000000000000120")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake", type="build")

    depends_on("py-numpy", type="run")

    depends_on("mpi")
    depends_on("callpath")
