# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Fluxbox(AutotoolsPackage):
    """Fluxbox is a windowmanager for X that was based on the Blackbox 0.61.1 code.

    It is very light on resources and easy to handle but yet full of features
    to make an easy, and extremely fast, desktop experience.
    """

    homepage = "http://fluxbox.org/"
    url      = "http://sourceforge.net/projects/fluxbox/files/fluxbox/1.3.7/fluxbox-1.3.7.tar.gz"

    version('1.3.7', 'd99d7710f9daf793e0246dae5304b595')

    depends_on('pkgconfig', type='build')
    depends_on('freetype')
    depends_on('libxrender')
    depends_on('libxext')
    depends_on('expat')
    depends_on('libx11')
