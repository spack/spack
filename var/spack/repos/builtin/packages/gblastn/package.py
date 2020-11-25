# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gblastn(AutotoolsPackage):
    """G-BLASTN is a GPU-accelerated nucleotide alignment tool
    based on the widely used NCBI-BLAST."""

    homepage = "https://github.com/OpenHero/gblastn"
    url      = "https://github.com/OpenHero/gblastn/tarball/22dab395e6ec0d749ae0c47e3898eb2d7862b4ed"

    version('22dab395e6ec0d749ae0c47e3898eb2d7862b4ed', sha256='d9aeefcb327c36e0379723692141c92d7621ce27196fcdc1817ff8dd2a79cac4')

    depends_on('cuda@10.1:')

    configure_directory = 'c++'

    def configure_args(self):
        args = [
                '--without-debug',
                '--with-mt',
                '--without-sybase',
                '--without-fastcgi',
                '--without-sssdb',
                '--without-sss',
                '--without-geo',
                '--without-sp',
                '--without-orbacus',
                '--without-boost']
        return args

