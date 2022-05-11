# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyPooch(PythonPackage):
    """Pooch manages your Python library's sample data files: it automatically
    downloads and stores them in a local directory, with support for versioning
    and corruption checks."""

    homepage = "https://github.com/fatiando/pooch"
    pypi     = "pooch/pooch-1.3.0.tar.gz"

    version('1.5.2', sha256='5969b2f1defbdc405df932767e05e0b536e2771c27f1f95d7f260bc99bf13581')
    version('1.3.0', sha256='30d448e825904e2d763bbbe418831a788813c32f636b21c8d60ee5f474532898')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', when='@1.4:', type='build')
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-packaging', type=('build', 'run'))
    depends_on('py-appdirs', type=('build', 'run'))
