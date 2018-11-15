# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Daligner(MakefilePackage):
    """Daligner: The Dazzler "Overlap" Module."""

    homepage = "https://github.com/thegenemyers/DALIGNER"
    url      = "https://github.com/thegenemyers/DALIGNER/archive/V1.0.tar.gz"

    version('1.0', 'f1b4c396ae062caa4c0e6423ba0725ef')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        kwargs = {'ignore_absent': False, 'backup': False, 'string': True}
        makefile.filter('cp $(ALL) ~/bin',
                        'cp $(ALL) {0}'.format(prefix.bin),
                        **kwargs)
        # He changed the Makefile in commit dae119.
        # You'll need this instead if/when he cuts a new release
        # or if you try to build from the tip of master.
        # makefile.filter('DEST_DIR = .*',
        #                'DEST_DIR = {0}'.format(prefix.bin))
        # or pass DEST_DIR in to the make

    @run_before('install')
    def make_prefix_dot_bin(self):
        mkdir(prefix.bin)
