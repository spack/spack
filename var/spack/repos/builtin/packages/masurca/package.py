# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Masurca(Package):
    """MaSuRCA is whole genome assembly software. It combines the efficiency
       of the de Bruijn graph and Overlap-Layout-Consensus (OLC)
       approaches."""

    homepage = "http://www.genome.umd.edu/masurca.html"
    version('3.3.1', sha256='587d0ee2c6b9fbd3436ca2a9001e19f251b677757fe5e88e7f94a0664231e020',
            url="https://github.com/alekseyzimin/masurca/releases/download/v3.3.1/MaSuRCA-3.3.1.tar.gz")

    version('3.3.0', sha256='8ad2fde3d7ebf15366212a3d4d02931f9767d85092392394acf91cd07ed63aac',
            url="https://github.com/alekseyzimin/masurca/releases/download/v3.3.0/MaSuRCA-3.3.0.tar.gz")

    version('3.2.9', sha256='795ad4bd42e15cf3ef2e5329aa7e4f2cdeb7e186ce2e350a45127e319db2904b',
            url="https://github.com/alekseyzimin/masurca/releases/download/3.2.9/MaSuRCA-3.2.9.tar.gz")

    version('3.2.8', sha256='b9ab27803d2a0bd8426b5c2e949874e9bc31c9cca8f7f0c8b487664d04cd0fe8',
            url="https://github.com/alekseyzimin/masurca/releases/download/3.2.8/MaSuRCA-3.2.8.tar.gz")

    version('3.2.7', sha256='3d3df9276d221551fd190cad3d037d56ce70691592cb28198e7bffc7c07760b2',
            url="https://github.com/alekseyzimin/masurca/releases/download/3.2.7/MaSuRCA-3.2.7.tar.gz")

    version('3.2.6', sha256='7c1fe3e96ca697043e31a559ae6da847ffaf699643472ad52b3febaf4ca93e25',
            url="https://github.com/alekseyzimin/masurca/releases/download/3.2.6/MaSuRCA-3.2.6.tar.gz")

    version('3.2.4', sha256='759d5b0411b048d996df1ca6daadf1cc49ff88f4436a21cd81d7f191a8bd80b0',
            url="https://github.com/alekseyzimin/masurca/files/1668918/MaSuRCA-3.2.4.tar.gz")

    depends_on('perl', type=('build', 'run'))
    depends_on('boost')
    depends_on('zlib')

    def install(self, spec, prefix):
        installer = Executable('./install.sh')
        installer()
        install_tree('.', prefix)
