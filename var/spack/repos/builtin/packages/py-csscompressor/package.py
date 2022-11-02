# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCsscompressor(PythonPackage):
    """A python port of YUI CSS Compressor."""

    pypi = "csscompressor/csscompressor-0.9.5.tar.gz"

    #maintainers = ["wscullin"]

    version("0.9.5", sha256="afa22badbcf3120a4f392e4d22f9fff485c044a1feda4a950ecc5eba9dd31a05")

