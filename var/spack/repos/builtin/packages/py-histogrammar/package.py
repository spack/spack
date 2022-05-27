# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHistogrammar(PythonPackage):
    """Composable histogram primitives for distributed data reduction."""

    homepage = "https://histogrammar.github.io/histogrammar-docs"
    pypi     = "histogrammar/histogrammar-1.0.25.tar.gz"

    version('1.0.25', sha256='01d5f99cdb8dce8f02dd1adbfcc530a097154f3696d7778d0ed596d06d5ce432')

    depends_on('python@3.6:',       type=('build', 'run'))
    depends_on('py-setuptools',     type='build')
    depends_on('py-numpy@1.18.0:',  type=('build', 'run'))
    depends_on('py-tqdm',           type=('build', 'run'))
    depends_on('py-joblib@0.14.0:', type=('build', 'run'))
