# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Spades(CMakePackage):
    """SPAdes - St. Petersburg genome assembler - is intended for both
       standard isolates and single-cell MDA bacteria assemblies."""

    homepage = "http://cab.spbu.ru/software/spades/"
    url      = "https://github.com/ablab/spades/releases/download/v3.15.0/SPAdes-3.15.0.tar.gz"

    version('3.15.0', sha256='6719489fa4bed6dd96d78bdd4001a30806d5469170289085836711d1ffb8b28b')
    version('3.14.1', sha256='d629b78f7e74c82534ac20f5b3c2eb367f245e6840a67b9ef6a76f6fac5323ca')
    version('3.14.0', sha256='18988dd51762863a16009aebb6e873c1fbca92328b0e6a5af0773e2b1ad7ddb9')
    version('3.13.1', sha256='8da29b72fb56170dd39e3a8ea5074071a8fa63b29346874010b8d293c2f72a3e')

    depends_on('python', type=('build', 'run'))
    depends_on('zlib')
    depends_on('bzip2')

    # SPAdes will explicitly not compile with gcc < 5.3.0
    conflicts('%gcc@:5.2.9')

    conflicts('%gcc@7.1.0:', when='@:3.10.1')

    root_cmakelists_dir = "src"
