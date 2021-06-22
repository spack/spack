# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Barvinok(AutotoolsPackage):
    """barvinok is a library for counting the number of integer points in parametric and
    non-parametric polytopes."""

    homepage = "http://barvinok.gforge.inria.fr"
    url      = "http://barvinok.gforge.inria.fr/barvinok-0.41.5.tar.bz2"

    version('0.41.5', sha256='e70493318fe76c0c202f98d7861bdf5dda8c4d79c21024af2e04b009ffa79734')

    depends_on('gmp')

    def configure_args(self):
        return [
            '--with-gmp-prefix={0}'.format(self.spec['gmp'].prefix)
        ]
