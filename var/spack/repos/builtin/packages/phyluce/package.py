# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Phyluce(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://github.com/faircloth-lab/phyluce/archive/v1.6.7.tar.gz"

    version('1.6.7', sha256='98c213ab1610506722ad1440ffc93f9cbc78d8b3aaf3d9a47837e1231452cdb6')

    extends('python')
    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-biopython', type='run')

    # runtime binary dependencies
    depends_on('abyss', type='run')
    depends_on('bcftools', type='run')
    depends_on('bwa', type='run')
    depends_on('gatk', type='run')
    depends_on('gblocks', type='run')
    depends_on('lastz', type='run')
    depends_on('mafft', type='run')
    depends_on('muscle', type='run')
    depends_on('picard', type='run')
    depends_on('raxml+pthreads+sse', type='run')
    depends_on('samtools', type='run')
    depends_on('seqtk', type='run')
    depends_on('spades', type='run')
    depends_on('trimal', type='run')
    depends_on('trinity', type='run')
    depends_on('velvet', type='run')

    def install(self, spec, prefix):
        python = which('python')
        python('setup.py', 'install', '--prefix={0}'.format(prefix))
