# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyani(PythonPackage):
    """pyani is a Python3 module that provides support for calculating
    average nucleotide identity (ANI) and related measures for whole genome
    comparisons, and rendering relevant graphical summary output. Where
    available, it takes advantage of multicore systems, and can integrate
    with SGE/OGE-type job schedulers for the sequence comparisons."""

    homepage = "http://widdowquinn.github.io/pyani"
    url      = "https://pypi.io/packages/source/p/pyani/pyani-0.2.7.tar.gz"

    version('0.2.7', '239ba630d375a81c35b7c60fb9bec6fa')
    version('0.2.6', 'd5524b9a3c62c36063ed474ea95785c9')

    depends_on('python@3.5:')
    depends_on('py-setuptools', type='build')
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-seaborn',    type=('build', 'run'))

    # Required for ANI analysis
    depends_on('py-biopython',  type=('build', 'run'))
    depends_on('py-pandas',     type=('build', 'run'))
    depends_on('py-scipy',      type=('build', 'run'))

    # Required for ANIb analysis
    depends_on('blast-plus~python', type='run')

    # Required for ANIm analysis
    depends_on('mummer', type='run')
