# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Aspell6De(AspellDictPackage):
    """German (de) dictionary for aspell."""

    homepage = "http://aspell.net/"
    url      = "https://ftpmirror.gnu.org/aspell/dict/de/aspell6-de-20030222-1.tar.bz2"

    version('6-de-20030222-1', '5950c5c8a36fc93d4d7616591bace6a6')
