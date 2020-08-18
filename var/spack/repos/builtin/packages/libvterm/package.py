# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libvterm(Package):
    """An abstract library implementation of a terminal emulator"""
    homepage = "http://www.leonerd.org.uk/code/libvterm/"
    url      = "http://www.leonerd.org.uk/code/libvterm/libvterm-0.1.3.tar.gz"

    version('0.1.3', preferred=True, sha256='e41724466a4658e0f095e8fc5aeae26026c0726dce98ee71d6920d06f7d78e2b')
    version('0.0.726', sha256='6344eca01c02e2270348b79e033c1e0957028dbcd76bc784e8106bea9ec3029d')
    version('0.0.681', sha256='abea46d1b0b831dec2af5d582319635cece63d260f8298d9ccce7c1c2e62a6e8')

    depends_on('libtool', type='build')

    def url_for_version(self, version):
        urlbase = "http://www.leonerd.org.uk/code/libvterm/"
        if version < Version('0.1'):
            snapshot = version.string.replace('0.0.', '')
            url = urlbase + "libvterm-0+bzr{0}.tar.gz".format(snapshot)
        else:
            url = urlbase + "libvterm-{0}.tar.gz".format(version)
        return url

    def install(self, spec, prefix):
        make()
        make("install", "PREFIX=" + prefix)
