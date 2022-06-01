# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BdwGc(AutotoolsPackage):
    """The Boehm-Demers-Weiser conservative garbage collector is a garbage
    collecting replacement for C malloc or C++ new."""

    homepage = "https://www.hboehm.info/gc/"
    url      = "https://github.com/ivmai/bdwgc/releases/download/v8.0.6/gc-8.0.6.tar.gz"

    version('8.0.6', sha256='3b4914abc9fa76593596773e4da671d7ed4d5390e3d46fbf2e5f155e121bea11')
    version('8.0.0', sha256='8f23f9a20883d00af2bff122249807e645bdf386de0de8cbd6cce3e0c6968f04')
    version('7.6.0', sha256='a14a28b1129be90e55cd6f71127ffc5594e1091d5d54131528c24cd0c03b7d90')
    version('7.4.4', sha256='e5ca9b628b765076b6ab26f882af3a1a29cde786341e08b9f366604f74e4db84')

    variant('libatomic-ops', default=True,
            description='Use external libatomic-ops')
    variant(
        'threads',
        default='none',
        values=('none', 'posix', 'dgux386'),
        multi=False,
        description='Multithreading support'
    )

    depends_on('libatomic-ops', when='+libatomic-ops')

    def configure_args(self):
        spec = self.spec

        config_args = [
            '--enable-static',
            '--with-libatomic-ops={0}'.format(
                'yes' if '+libatomic-ops' in spec else 'no'),
            "--enable-threads={0}".format(spec.variants['threads'].value)
        ]

        return config_args
