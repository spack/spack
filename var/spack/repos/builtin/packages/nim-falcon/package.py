# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os


class NimFalcon(Package):
    """nim-falcon: Nim versions of FALCON executables"""

    homepage = "https://github.com/bio-nim/nim-falcon"
    git      = "https://github.com/bio-nim/nim-falcon.git"

    version('2019.05.22',
           commit='5cb3c47d6ae76866f8d648da184177f2c803053b')

    depends_on('ccache',      type=('build'))
    depends_on('nim@0.19.9',  type=('build'))

    def install(self, spec, prefix):
        os.environ['NIMBLE_DIR'] = os.getcwd() + '/nimble_dir'
        make('update')
        make('install')

        nimble_bin = os.environ.get('NIMBLE_DIR') + '/bin'
        install_tree(nimble_bin, prefix.bin, symlinks=False)
