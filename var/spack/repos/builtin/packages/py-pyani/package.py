# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
    pypi = "pyani/pyani-0.2.7.tar.gz"

    version('0.2.10', sha256='154e421c52125d3bf309c96cfcfd0defba4b990a14cc7fdac89a8b31e5b22b59')
    version('0.2.9',  sha256='0b87870a03cf5ccd8fbab7572778903212a051990f00cf8e4ef5887b36b9ec91')
    version('0.2.8',  sha256='8059f3ede59225d0cb81ddc4d7193c1744b3732a548fa05b09c5992c27837345')
    version('0.2.7', sha256='dbc6c71c46fbbfeced3f8237b84474221268b51170caf044bec8559987a7deb9')
    version('0.2.6', sha256='e9d899bccfefaabe7bfa17d48eef9c713d321d2d15465f7328c8984807c3dd8d')

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
