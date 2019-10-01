# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OntAlbacore(Package):
    """Albacore is a software project that provides an entry point to the Oxford
    Nanopore basecalling algorithms. It can be run from the command line on
    Windows and multiple Linux platforms. A selection of configuration files
    allow basecalling DNA libraries made with our current range of sequencing
    kits and Flow Cells."""

    homepage = "https://nanoporetech.com"
    url = "https://mirror.oxfordnanoportal.com/software/analysis/ont_albacore-2.3.1-cp35-cp35m-manylinux1_x86_64.whl"

    version('2.3.1', '0e85ad176e691252344c4c4b673c4b68', expand=False)
    version('2.1.2', '1e60cfb95628829f2a61a85247f1b6af', expand=False)
    version('1.2.4', '559640bec4693af12e4d923e8d77adf6', expand=False)
    version('1.1.0', 'fab4502ea1bad99d813aa2629e03e83d', expand=False)
    extends('python')

    depends_on('python@3.5.0:3.5.999', type=('build', 'run'))
    depends_on('py-setuptools',        type=('build', 'run'))
    depends_on('py-numpy@1.13.0',      type=('build', 'run'))
    depends_on('py-python-dateutil',   type=('build', 'run'))
    depends_on('py-h5py',              type=('build', 'run'))
    depends_on('py-ont-fast5-api',     type=('build', 'run'))
    depends_on('py-pip',               type=('build'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
