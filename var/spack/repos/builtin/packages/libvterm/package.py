# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libvterm(Package):
    """An abstract library implementation of a terminal emulator"""
    homepage = "http://www.leonerd.org.uk/code/libvterm/"
    url      = "http://www.leonerd.org.uk/code/libvterm/libvterm-0+bzr681.tar.gz"

    version('681', '7a4325a7350b7092245c04e8ee185ac3')

    depends_on('libtool', type='build')

    def install(self, spec, prefix):
        make()
        make("install", "PREFIX=" + prefix)
