# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bcftools(AutotoolsPackage):
    """BCFtools is a set of utilities that manipulate variant calls in the
       Variant Call Format (VCF) and its binary counterpart BCF. All
       commands work transparently with both VCFs and BCFs, both
       uncompressed and BGZF-compressed."""

    homepage = "http://samtools.github.io/bcftools/"
    url      = "https://github.com/samtools/bcftools/releases/download/1.3.1/bcftools-1.3.1.tar.bz2"

    version('1.8', 'ba6c2fb7eb6dcb208f00ab8b22df475c')
    version('1.7', 'c972db68d17af9da3a18963f4e5aeca8')
    version('1.6', 'c4dba1e8cb55db0f94b4c47724b4f9fa')
    version('1.4', '50ccf0a073bd70e99cdb3c8be830416e')
    version('1.3.1', '575001e9fca37cab0c7a7287ad4b1cdb')
    version('1.2', '8044bed8fce62f7072fc6835420f0906')

    depends_on('libzip', when='@1.8:')

    depends_on('htslib@1.8', when='@1.8')
    depends_on('htslib@1.7',   when='@1.7')
    depends_on('htslib@1.6',   when='@1.6')
    depends_on('htslib@1.4',   when='@1.4')
    depends_on('htslib@1.3.1', when='@1.3.1')
    depends_on('htslib@1.2', when='@1.2')
