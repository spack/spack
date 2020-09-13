# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTombo(PythonPackage):
    """Tombo is a suite of tools primarily for the identification of
    modified nucleotides from nanopore sequencing data. Tombo also
    provides tools for the analysis and visualization of raw nanopore
    signal."""

    homepage = "https://nanoporetech.github.io/tombo/"
    url      = "https://github.com/nanoporetech/tombo/archive/1.5.1.tar.gz"

    version('1.5.1', sha256='f5f7ce37baee40b851ea867c2b835e6eae324ef90bdeb23fb931fde3272769a0')
    version('1.5',   sha256='51de9a86f99d2117aeee20fabb73470f649d29a6d79a40925f3f7348118aae98')
    version('1.4',   sha256='af478a046156e8644fbf458191da18e2757fd71ac91d645c13cd5a3b5006c695')

    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-cython', type=('build', 'run'))
    depends_on('py-future', type=('build', 'run'))
    depends_on('py-tqdm', type=('build', 'run'))
    depends_on('py-pyfaidx', type=('build', 'run'))
    depends_on('minimap2', type=('build', 'run'))
    depends_on('py-rpy2@:2.8.6', type=('build', 'run'), when='^python@:2.9.99')
    depends_on('py-rpy2@:2.9.5', type=('build', 'run'), when='^python@3:')
