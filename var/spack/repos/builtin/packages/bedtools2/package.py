# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bedtools2(Package):
    """Collectively, the bedtools utilities are a swiss-army knife of
       tools for a wide-range of genomics analysis tasks. The most
       widely-used tools enable genome arithmetic: that is, set theory
       on the genome."""

    homepage = "https://github.com/arq5x/bedtools2"
    url      = "https://github.com/arq5x/bedtools2/archive/v2.26.0.tar.gz"

    version('2.29.2', sha256='bc2f36b5d4fc9890c69f607d54da873032628462e88c545dd633d2c787a544a5')
    version('2.27.1', sha256='c8c2acbaf3f9cb92dcf8e5cd59af6b31ae9c4598efb786ba6c84f66ca72fafd9')
    version('2.27.0', sha256='e4f0e5616d04ba5ac09c36dec989b1236a5712e67d0b6874ff5e144d7ed4ce60')
    version('2.26.0', sha256='65f32f32cbf1b91ba42854b40c604aa6a16c7d3b3ec110d6acf438eb22df0a4a')
    version('2.25.0', sha256='d737ca42e7df76c5455d3e6e0562cdcb62336830eaad290fd4133a328a1ddacc')
    version('2.24.0', sha256='ea73b8620468c5a15d4ed96dc98c83e5564880bb9651cd75f1dcc96694be60e4')
    version('2.23.0', sha256='3386b2989550dde014607cad312e8fecbdc942eacbb1c60c5cdac832e3eae251')

    depends_on('zlib')
    depends_on('python', type='build')

    def install(self, spec, prefix):
        make("prefix=%s" % prefix, "install")
