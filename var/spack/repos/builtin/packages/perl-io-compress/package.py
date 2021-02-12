# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlIoCompress(PerlPackage):
    """A perl library for uncompressing gzip, zip, bzip2
    or lzop file/buffer."""

    homepage = "http://search.cpan.org/~pmqs/IO-Compress-2.070/lib/IO/Uncompress/AnyUncompress.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/IO-Compress-2.081.tar.gz"

    version('2.100', sha256='2d23b0be2e2967c604c407d415588920a69083587d0f65f355137592989c6c36')
    version('2.096', sha256='9d219fd5df4b490b5d2f847921e3cb1c3392758fa0bae9b05a8992b3620ba572')
    version('2.095', sha256='90e064ca2e8f1f1ecb2ace6105209596f7860cbf446a7ee29e08987e36f65793')
    version('2.094', sha256='7d6156333b12c57aa4cc023dd4d127c0fa33c7ad0eed54b84db9fa9ddca6c0b9')
    version('2.093', sha256='5f8f5d06913f16c16759cc4e06749692208b8947910ffedd2c00a74ed0d60ba2')
    version('2.092', sha256='994575e39aff933b06ea14f16be80d073e08db1ebd54e1cb07566f2b0aed50b3')
    version('2.091', sha256='1f0d1190b13736445c92b6e10617928d86b3dfa1a2b4bf5769f3eb5eb7a45e95')
    version('2.090', sha256='4c12e54a83f993372d43dd67389a1ca92b5c33c108c7f86768a4797cd994e987')
    version('2.089', sha256='2d3474fc34cf729660a92c481ed7a141434389a36af9c8341603945e11bc5005')
    version('2.088', sha256='9d4a390486fb7a8e23c7b235255367b983407e0633ca9e2e17d53e54ea95a8cd')
    version('2.087', sha256='94f792775d0496fffe862363c76637e74ff5b46c40cf47042547686d164e23cb')
    version('2.086', sha256='110a229aa02b701f9820f5e0c2e9c30db342ea241b2d01c03703ea4922b1ab53')
    version('2.084', sha256='1dbd503eda643aa58d1ef9b4d44c57889243d0ce6c54d5b45babceb860d76db5')
    version('2.083', sha256='43be5ff880d2f27d7320f156cce9774d446f14a33d9afd57892b81e17657e4cc')
    version('2.081', sha256='5211c775544dc8c511af08edfb1c0c22734daa2789149c2a88d68e17b43546d9')

    depends_on('perl-compress-raw-zlib', type='run')
    depends_on('perl-compress-raw-bzip2', type='run')
