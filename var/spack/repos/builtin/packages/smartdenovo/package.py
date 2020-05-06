# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Smartdenovo(MakefilePackage):
    """SMARTdenovo is a de novo assembler for PacBio and Oxford Nanopore
    (ONT) data."""

    homepage = "https://github.com/ruanjue/smartdenovo"
    git      = "https://github.com/ruanjue/smartdenovo.git"

    version('master', branch='master')

    depends_on('sse2neon', when='target=aarch64:')

    patch('aarch64.patch', when='target=aarch64:',
        sha256='7dd4bca28aafb0680cc1823aa58ac9000819993538e92628554666c4b3acc470')

    def install(self, spec, prefix):
        install_files = [
            'pairaln', 'wtpre', 'wtcyc', 'wtmer', 'wtzmo', 'wtobt',
            'wtclp', 'wtext', 'wtgbo', 'wtlay', 'wtcns', 'wtmsa'
        ]
        mkdirp(prefix.bin)
        for f in install_files:
            install(f, prefix.bin)
