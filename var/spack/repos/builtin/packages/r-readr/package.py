# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RReadr(RPackage):
    """Read Rectangular Text Data

    The goal of 'readr' is to provide a fast and friendly way to read
    rectangular data (like 'csv', 'tsv', and 'fwf'). It is designed to flexibly
    parse many types of data found in the wild, while still cleanly failing
    when data unexpectedly changes."""

    homepage = "https://cloud.r-project.org/package=readr"
    cran = "readr"

    version('2.0.2', sha256='98b05ed751dda2bcf7a29d070ce3d3e8475e0138a3e3ec68941dc45218db7615')
    version('1.4.0', sha256='02b1188aab8b2bc3f3d2bba5b946bd299610e87f3f7660c88b60b444093c46b9')
    version('1.3.1', sha256='33f94de39bb7f2a342fbb2bd4e5afcfec08798eac39672ee18042ac0b349e4f3')
    version('1.1.1', sha256='1a29b99009a06f2cee18d08bc6201fd4985b6d45c76cefca65084dcc1a2f7cb3')

    depends_on('r@3.0.2:', when='@:1.2.1', type=('build', 'run'))
    depends_on('r@3.1:', when='@1.3.0:', type=('build', 'run'))
    depends_on('r-cli', when='@1.4.0:', type=('build', 'run'))
    depends_on('r-clipr', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-crayon', when='@1.3.1:', type=('build', 'run'))
    depends_on('r-hms@0.4.1:', type=('build', 'run'))
    depends_on('r-rlang', when='@1.4.0:', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-vroom@1.5.2:', when='@2.0.0', type=('build', 'run'))
    depends_on('r-vroom@1.5.4:', when='@2.0.1:', type=('build', 'run'))
    depends_on('r-lifecycle', when='@1.4.0:', type=('build', 'run'))
    depends_on('r-lifecycle@0.2.0:', when='@2:', type=('build', 'run'))
    depends_on('r-cpp11', when='@1.4.0:', type=('build', 'run'))
    depends_on('r-tzdb@0.1.1:', when='@2:', type=('build', 'run'))

    depends_on('r-bh', when='@:1', type=('build', 'run'))
    depends_on('r-rcpp@0.12.0.5:', when='@:1.3.1', type=('build', 'run'))
