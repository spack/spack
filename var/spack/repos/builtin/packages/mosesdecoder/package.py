# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Mosesdecoder(Package):
    """An implementation of the statistical approach to machine translation"""

    homepage = "http://www2.statmt.org/moses/"
    url = "https://github.com/moses-smt/mosesdecoder/archive/refs/tags/RELEASE-4.0.tar.gz"

    version("4.0", sha256="357376cdbb225a17cdf17195625d0fa7e10d722807e9e0b8a633ffbd7eec9b8f")

    depends_on("git")
    depends_on("subversion")
    depends_on("cmake")
    depends_on("libtool")
    depends_on("tcl")
    depends_on("gcc")
    depends_on("boost")
    depends_on("zlib")
    depends_on("python")
