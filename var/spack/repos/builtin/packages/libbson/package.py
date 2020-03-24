# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libbson(AutotoolsPackage):
    """libbson is a library providing useful routines related to building,
    parsing, and iterating BSON documents."""

    homepage = "https://github.com/mongodb/libbson"
    url      = "https://github.com/mongodb/libbson/releases/download/1.7.0/libbson-1.7.0.tar.gz"

    maintainers = ['michaelkuhn']

    version('1.9.1', sha256='236d9fcec0fe419c2201481081e497f49136eda2349b61cfede6233013bf7601')
    version('1.8.1', sha256='9d18d14671b7890e27b2a5ce33a73a5ed5d33d39bba70209bae99c1dc7aa1ed4')
    version('1.8.0', sha256='63dea744b265a2e17c7b5e289f7803c679721d98e2975ea7d56bc1e7b8586bc1')
    version('1.7.0', sha256='442d89e89dfb43bba1f65080dc61fdcba01dcb23468b2842c1dbdd4acd6049d3')
    version('1.6.3', sha256='e9e4012a9080bdc927b5060b126a2c82ca11e71ebe7f2152d079fa2ce461a7fb')
    version('1.6.2', sha256='aad410123e4bd8a9804c3c3d79e03344e2df104872594dc2cf19605d492944ba')
    version('1.6.1', sha256='5f160d44ea42ce9352a7a3607bc10d3b4b22d3271763aa3b3a12665e73e3a02d')

    depends_on('autoconf', type='build', when='@1.6.1')
    depends_on('automake', type='build', when='@1.6.1')
    depends_on('libtool', type='build', when='@1.6.1')
    depends_on('m4', type='build', when='@1.6.1')

    @property
    def force_autoreconf(self):
        # 1.6.1 tarball is broken
        return self.spec.satisfies('@1.6.1')
