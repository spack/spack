# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTetoolkit(PythonPackage):
    """TEToolkit is a software package that utilizes both unambiguously
       (uniquely) and ambiguously (multi-) mapped reads to perform
       differential enrichment analyses from high throughput sequencing
       experiments."""

    homepage = "http://hammelllab.labsites.cshl.edu/software"
    url      = "https://pypi.io/packages/source/T/TEToolkit/TEToolkit-1.5.1.tar.gz"

    version('1.5.1', '05745b2d5109911e95593e423446a831')

    depends_on('py-setuptools')
    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-pysam', type=('build', 'run'))
    depends_on('r-deseq', type=('build', 'run'))
