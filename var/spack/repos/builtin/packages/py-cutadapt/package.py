# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCutadapt(PythonPackage):
    """Cutadapt finds and removes adapter sequences, primers, poly-A tails and
    other types of unwanted sequence from your high-throughput sequencing
    reads."""

    homepage = "https://cutadapt.readthedocs.io"
    url      = "https://pypi.io/packages/source/c/cutadapt/cutadapt-1.13.tar.gz"

    version('1.13', '2d2d14e0c20ad53d7d84b57bc3e63b4c')

    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-xopen@0.1.1:', type=('build', 'run'))
