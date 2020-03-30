# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Garply(Package):
    """Toy package for testing dependencies"""

    homepage = "https://www.example.com"
    url      = "https://github.com/gartung/garply/releases/download/v3.0.0/garply-3.0.0.tar.gz"

    version(
        '3.0.0', sha256='f3d5fbfc69f764addf472298c0af905df7255d823ddb7a79bd4c2400794b3941',
         url="https://github.com/gartung/garply/releases/download/v3.0.0/garply-3.0.0.tar.gz")

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)
        patchelf = which('patchelf')
        rpaths = '%s:%s' % (prefix.lib64, prefix.lib)
        patchelf('--force-rpath', '--set-rpath', rpaths, '%s/garplinator' %
                 prefix.lib64)
        patchelf('--force-rpath', '--set-rpath', rpaths, '%s/libgarply.so' %
                 prefix.lib64)
