# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cairomm(AutotoolsPackage):
    """Cairomm is a C++ wrapper for the cairo graphics library."""

    homepage = "https://www.cairographics.org/cairomm/"
    url      = "https://cairographics.org/releases/cairomm-1.6.4.tar.gz"

    version('1.6.4', '63561c62536173a98f03005dfe55c90e')
    version('1.6.2', 'eac5d159e4cba98e32ea174483dee24e')

    depends_on('cairo')
    depends_on('libsigcpp')
