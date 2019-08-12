# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pandaseq(AutotoolsPackage):
    """PANDASEQ is a program to align Illumina reads, optionally with PCR
    primers embedded in the sequence, and reconstruct an overlapping
    sequence."""

    homepage = "https://github.com/neufeld/pandaseq"
    url      = "https://github.com/neufeld/pandaseq/archive/v2.11.tar.gz"

    version('2.11', 'a8ae0e938bac592fc07dfa668147d80b')
    version('2.10', '5b5b04c9b693a999f10a9c9bd643f068')

    depends_on('autoconf',    type='build')
    depends_on('automake',    type='build')
    depends_on('libtool',     type=('build', 'link'))
    depends_on('m4',          type='build')
    depends_on('zlib',        type='build')
    depends_on('pkgconfig',   type='build')
    depends_on('bzip2',       type='link')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')
