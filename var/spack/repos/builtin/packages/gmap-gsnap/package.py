# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GmapGsnap(AutotoolsPackage):
    """GMAP: A Genomic Mapping and Alignment Program for
       mRNA and EST Sequences, and GSNAP: Genomic Short-read
       Nucleotide Alignment Program"""

    homepage = "http://research-pub.gene.com/gmap/"
    url      = "http://research-pub.gene.com/gmap/src/gmap-gsnap-2017-06-16.tar.gz"

    version('2019-05-12', sha256='3dc1b6ee4f6c049c07bcf4a5aba30eb2d732997241cdcad818dab571719f8008')
    version('2019-02-15', sha256='7e82b9867a1e561b4816fb2f2fb916294077c384c6a88bb94cce39bfe71ab3ac')
    version('2018-07-04', sha256='a9f8c1f0810df65b2a089dc10be79611026f4c95e4681dba98fea3d55d598d24')
    version('2018-03-25', 'f08e65c1e4d9574a3eb7f15f8ca6af16')
    version('2018-02-12', '13152aedeef9ac66be915fc6bf6464f2')
    version('2017-06-16', 'fcc91b8bdd4bf12ae3124de0c00db0c0')
    version('2014-12-28', '1ab07819c9e5b5b8970716165ccaa7da')

    depends_on('zlib')
    depends_on('bzip2')

    variant(
        'simd',
        description='CPU support.',
        values=('avx2', 'sse42', 'avx512', 'sse2'),
        multi=True,
        default='sse2'
    )

    def configure(self, spec, prefix):
        configure = Executable('../configure')

        for simd in spec.variants['simd'].value:
            with working_dir(simd, create=True):
                configure('--with-simd-level={0}'.format(simd),
                          '--prefix={0}'.format(prefix))

    def build(self, spec, prefix):
        for simd in spec.variants['simd'].value:
            with working_dir(simd):
                make()

    def check(self):
        for simd in self.spec.variants['simd'].value:
            with working_dir(simd):
                make('check')

    def install(self, spec, prefix):
        for simd in spec.variants['simd'].value:
            with working_dir(simd):
                make('install')
