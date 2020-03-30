# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Corge(Package):
    """A toy package to test dependencies"""

    homepage = "https://www.example.com"
    url      = "https://github.com/gartung/corge/releases/download/v3.0.0/corge-3.0.0.tar.gz"

    version(
        '3.0.0', sha256='5d64e03c48843a9af51e81464e46b148cf0a1529977c4d0bb543daa8a906e862',
        url="https://github.com/gartung/corge/releases/download/v3.0.0/corge-3.0.0.tar.gz")

    depends_on('quux')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)
        patchelf = which('patchelf')
        rpaths = '%s:%s:%s:%s:%s:%s' % (prefix.lib, prefix.lib64,
                                        spec['quux'].prefix.lib,
                                        spec['quux'].prefix.lib64,
                                        spec['garply'].prefix.lib,
                                        spec['garply'].prefix.lib64)
        patchelf('--force-rpath', '--set-rpath', rpaths, '%s/corgegator' %
                 prefix.bin)
        patchelf('--force-rpath', '--set-rpath', rpaths, '%s/libcorge.so' %
                 prefix.lib64)
