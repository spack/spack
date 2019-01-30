# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class BdwGc(AutotoolsPackage):
    """The Boehm-Demers-Weiser conservative garbage collector is a garbage
    collecting replacement for C malloc or C++ new."""

    homepage = "http://www.hboehm.info/gc/"
    url      = "http://www.hboehm.info/gc/gc_source/gc-7.6.0.tar.gz"

    version('7.6.0', 'bf46ccbdaccfa3186c2ab87191c8855a')
    version('7.4.4', '96d18b0448a841c88d56e4ab3d180297')

    variant('libatomic-ops', default=True,
            description='Use external libatomic-ops')

    depends_on('libatomic-ops', when='+libatomic-ops')

    def configure_args(self):
        spec = self.spec

        config_args = [
            '--with-libatomic-ops={0}'.format(
                'yes' if '+libatomic-ops' in spec else 'no')
        ]

        return config_args
