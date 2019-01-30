# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySnowballstemmer(PythonPackage):
    """This package provides 16 stemmer algorithms (15 + Poerter
    English stemmer) generated from Snowball algorithms."""

    homepage = "https://github.com/shibukawa/snowball_py"
    url      = "https://pypi.io/packages/source/s/snowballstemmer/snowballstemmer-1.2.1.tar.gz"

    import_modules = ['snowballstemmer']

    version('1.2.1', '643b019667a708a922172e33a99bf2fa')
