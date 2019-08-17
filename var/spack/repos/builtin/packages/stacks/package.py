# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Stacks(AutotoolsPackage):
    """Stacks is a software pipeline for building loci from short-read
       sequences, such as those generated on the Illumina platform."""

    homepage = "http://catchenlab.life.illinois.edu/stacks/"
    url      = "http://catchenlab.life.illinois.edu/stacks/source/stacks-1.46.tar.gz"

    version('2.3b', sha256='a46786d8811a730ebcdc17891e89f50d4f4ae196734439dac86091f45c92ac72')
    version('1.46', '18b0568a4bba44fb4e5be0eb7ee2c08d')

    variant('sparsehash', default=True, description='Improve Stacks memory usage with SparseHash')

    depends_on('perl', type=('build', 'run'))
    depends_on('sparsehash', when='+sparsehash')
    depends_on('zlib', when='@2.3b:')
    conflicts('%gcc@:4.9.0', when='@2.3b:')

    def configure_args(self):
        args = []
        if '+sparsehash' in self.spec:
            args.append('--enable-sparsehash')
        else:
            args.append('--disable-sparsehash')
        return args
