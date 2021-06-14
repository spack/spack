# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Scrot(AutotoolsPackage):
    """scrot (SCReenshOT) is a simple command line screen
    capture utility that uses imlib2 to grab and save images.
    Multiple image formats are supported through imlib2's
    dynamic saver modules."""

    homepage = "https://github.com/resurrecting-open-source-projects/scrot"
    url      = "https://github.com/resurrecting-open-source-projects/scrot/archive/refs/tags/1.5.tar.gz"

    version('1.5', sha256='87afba3998aac097f13231f3b0452c21188bf4b5cc6ac0747693a1da1a0ae40f')

    depends_on('autoconf-archive', type='build')
    depends_on('automake', type='build')
    depends_on('giblib', when='@:1.5')  # @master already has this dependency removed
    depends_on('imlib2')
    depends_on('libtool')
    depends_on('libxcomposite')
    depends_on('libxfixes')
