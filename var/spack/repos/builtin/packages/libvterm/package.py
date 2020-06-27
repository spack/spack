# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libvterm(Package):
    """An abstract library implementation of a terminal emulator"""
    homepage = "http://www.leonerd.org.uk/code/libvterm/"
    url      = "http://www.leonerd.org.uk/code/libvterm/libvterm-0+bzr681.tar.gz"

    version('681', sha256='abea46d1b0b831dec2af5d582319635cece63d260f8298d9ccce7c1c2e62a6e8')

    depends_on('libtool', type='build')

    def install(self, spec, prefix):
        make()
        make("install", "PREFIX=" + prefix)
