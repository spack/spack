# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Aspell6En(AspellDictPackage):
    """English (en) dictionary for aspell."""

    homepage = "http://aspell.net/"
    url      = "https://ftpmirror.gnu.org/aspell/dict/en/aspell6-en-2017.01.22-0.tar.bz2"

    version('2017.01.22-0', 'a6e002076574de9dc4915967032a1dab')
