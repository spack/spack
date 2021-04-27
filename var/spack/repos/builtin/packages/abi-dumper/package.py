# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class AbiDumper(MakefilePackage):
    """ABI Dumper is a tool to dump ABI of an ELF object containing
    DWARF debug info."""

    homepage = "https://github.com/lvc/abi-dumper"
    url      = "https://github.com/lvc/abi-dumper/archive/1.1.tar.gz"

    version('1.1',     sha256='ef63201368e0d76a29d2f7aed98c488f6fb71898126762d65baed1e762988083')
    version('1.0',     sha256='bfa0189a172fa788afc603b1ae675808a57556a77a008e4af8f643d396c34bbb')
    version('0.99.19', sha256='6bbc35795839a04523d9e7bdb07806b9a661e17d8be0e755c99e4235805d4528')

    depends_on('perl@5:')
    depends_on('elfutils')
    depends_on('binutils')
    depends_on('universal-ctags')
    depends_on('vtable-dumper@1.1:')

    phases = ['install']

    def install(self, spec, prefix):
        make('prefix={0}'.format(prefix), 'install')
