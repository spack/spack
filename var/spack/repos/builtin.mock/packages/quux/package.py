# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Quux(Package):
    """Toy package for testing dependencies"""

    homepage = "https://www.example.com"
    url      = "https://github.com/gartung/quux/releases/download/v3.0.0/quux-3.0.0.tar.gz"

    version('3.0.0', sha256='b4fa6bc3216f490eeef93b3cf71586d8e9df30d8536fbae08b60ec1d7add4f05',
            url="https://github.com/gartung/quux/releases/download/v3.0.0/quux-3.0.0.tar.gz")

    depends_on('garply')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)
        patchelf = which('patchelf')
        rpaths = '%s:%s:%s:%s' % (prefix.lib, prefix.lib64,
                                  spec['garply'].prefix.lib,
                                  spec['garply'].prefix.lib64)
        patchelf('--force-rpath', '--set-rpath', rpaths, '%s/quuxifier' %
                 prefix.lib64)
        patchelf('--force-rpath', '--set-rpath', rpaths, '%s/libquux.so' %
                 prefix.lib64)
