# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Spades(CMakePackage):
    """SPAdes - St. Petersburg genome assembler - is intended for both
       standard isolates and single-cell MDA bacteria assemblies."""

    homepage = "http://cab.spbu.ru/software/spades/"
    url      = "http://cab.spbu.ru/files/release3.10.1/SPAdes-3.10.1.tar.gz"

    version('3.12.0', '15b48a3bcbbe6a8ad58fd04ba5d3f1015990fbfd9bdf4913042803b171853ac7')
    version('3.11.1', '478677b560e2f98db025e8efd5245cdf')
    version('3.10.1', 'dcab7d145af81b59cc867562f27536c3')

    depends_on('python', type=('build', 'run'))
    depends_on('zlib')
    depends_on('bzip2')

    conflicts('%gcc@7.1.0:', when='@:3.10.1')

    root_cmakelists_dir = 'src'
