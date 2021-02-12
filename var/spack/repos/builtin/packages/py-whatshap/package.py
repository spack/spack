# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWhatshap(PythonPackage):
    """WhatsHap is a software for phasing genomic variants using DNA
       sequencing reads, also called read-based phasing or haplotype
       assembly."""

    homepage = "https://whatshap.readthedocs.io/en/latest/"
    url      = "https://bitbucket.org/whatshap/whatshap/get/v0.17.tar.gz"

    version('1.0',  sha256='9a886729ae98f9d69814f589d6a4b7d57dae6d99013ef1104c67d72ebae1b09a')
    version('0.18', sha256='500b9ec9d67749e1c9a71bad4884dace4cfc8ea84524efa3c8a5005d726ce0c7')
    version('0.17', sha256='5f342cbd28f5d3e79490754f067aa67e8bb059da1c042d944b9f75663ef6b055')

    depends_on('python@3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-cython@0.17:', type=('build', 'run'))
    depends_on('py-pysam@0.14.0:', type='run')
    depends_on('py-xopen', type='run')
    depends_on('py-pyvcf', type='run')
    depends_on('py-pyfaidx', type='run')
    depends_on('py-networkx', type='run')

    def patch(self):
        # there is a stray \xe2 somewhere in setup.py,
        # explicitly using utf-8 will let the install proceed
        filter_file('^"""$', '#coding: utf-8\n"""', 'setup.py')
