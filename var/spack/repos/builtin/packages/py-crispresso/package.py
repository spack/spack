# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCrispresso(PythonPackage):
    """Software pipeline for the analysis of CRISPR-Cas9 genome editing
    outcomes from deep sequencing data."""

    homepage = "https://github.com/lucapinello/CRISPResso"
    url      = "https://pypi.io/packages/source/C/CRISPResso/CRISPResso-1.0.8.tar.gz"

    version('1.0.8', '2f9b52fe62cf49012a9525845f4aea45')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.7.0:2.7.999', type=('build', 'run'))
    depends_on('py-biopython@1.6.5:', type=('build', 'run'))
    depends_on('py-matplotlib@1.3.1:', type=('build', 'run'))
    depends_on('py-numpy@1.9:', type=('build', 'run'))
    depends_on('py-pandas@0.15:', type=('build', 'run'))
    depends_on('py-seaborn@0.7.1:', type=('build', 'run'))
    depends_on('emboss@6:', type=('build', 'run'))
    depends_on('flash', type=('build', 'run'))
    depends_on('java', type=('build', 'run'))
