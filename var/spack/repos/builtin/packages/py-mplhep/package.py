# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyMplhep(PythonPackage):
    """Matplotlib styles for HEP"""

    homepage = "https://github.com/scikit-hep/mplhep"
    pypi     = "mplhep/mplhep-0.3.15.tar.gz"

    version('0.3.15', sha256='595f796ea65930094e86a805214e0d44537ead267a7487ae16eda02d1670653e')

    depends_on('python@3.7:',        type=('build', 'run'))
    depends_on('py-setuptools@39.2:',      type='build')
    depends_on('py-mplhep-data',     type=('build', 'run'))
    depends_on('py-matplotlib@3.4:', type=('build', 'run'))
    depends_on('py-numpy@1.16.0:',   type=('build', 'run'))
    depends_on('py-packaging',       type=('build', 'run'))
    depends_on('py-uhi@0.2.0:',      type=('build', 'run'))
