# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bedops(MakefilePackage):
    """BEDOPS is an open-source command-line toolkit that performs highly
    efficient and scalable Boolean and other set operations, statistical
    calculations, archiving, conversion and other management of genomic data of
    arbitrary scale."""

    homepage = "https://bedops.readthedocs.io"
    url      = "https://github.com/bedops/bedops/archive/v2.4.30.tar.gz"

    version('2.4.35', 'b425b3e05fd4cd1024ef4dd8bf04b4e5')
    version('2.4.34', 'fc467d96134a0efe8b134e638af87a1a')
    version('2.4.30', '4e5d9f7b7e5432b28aef8d17a22cffab')

    @property
    def build_targets(self):
        # avoid static linking with glibc for all invocations
        return ['SFLAGS=']

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        make('install', "BINDIR=%s" % prefix.bin)
