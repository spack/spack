# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


# See also: AspellDictPackage
class Aspell(AutotoolsPackage):
    """GNU Aspell is a Free and Open Source spell checker designed to
    eventually replace Ispell."""

    homepage = "http://aspell.net/"
    url      = "https://ftpmirror.gnu.org/aspell/aspell-0.60.6.1.tar.gz"

    extendable = True           # support activating dictionaries

    version('0.60.6.1', sha256='f52583a83a63633701c5f71db3dc40aab87b7f76b29723aeb27941eff42df6e1')

    patch('darwin.patch', when='platform=darwin')
    patch('issue-519.patch', when='@:0.60.6.1')
