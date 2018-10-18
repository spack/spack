# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Isl(AutotoolsPackage):
    """isl (Integer Set Library) is a thread-safe C library for manipulating
    sets and relations of integer points bounded by affine constraints."""

    homepage = "http://isl.gforge.inria.fr"
    url      = "http://isl.gforge.inria.fr/isl-0.19.tar.bz2"

    version('0.19', '7850d46a96e5ea31e34913190895e154')
    version('0.18', '11436d6b205e516635b666090b94ab32')
    version('0.14', 'acd347243fca5609e3df37dba47fd0bb')

    depends_on('gmp')

    def configure_args(self):
        return [
            '--with-gmp-prefix={0}'.format(self.spec['gmp'].prefix)
        ]
