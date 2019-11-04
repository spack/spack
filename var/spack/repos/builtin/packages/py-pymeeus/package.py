# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPymeeus(PythonPackage):
    """Library of astronomical algorithms in Python."""

    homepage = "https://github.com/architest/pymeeus"
    url      = "https://pypi.io/packages/source/P/PyMeeus/PyMeeus-0.3.6.tar.gz"

    version('0.3.6', sha256='1f1ba0682e1b5c6b0cd6432c966e8bc8acc31737ea6f0ae79917a2189a98bb87')

    depends_on('py-setuptools', type='build')
    depends_on('py-atomicwrites@1.2.1:', type=('build', 'run'))
    depends_on('py-attrs@18.2.0:', type=('build', 'run'))
    depends_on('py-configparser@3.5.0:', type=('build', 'run'))
    depends_on('py-coverage@4.5.2:', type=('build', 'run'))
    depends_on('py-enum34@1.1.6:', type=('build', 'run'), when='^python@:3.3.99')
    depends_on('py-flake8@3.6.0:', type=('build', 'run'))
    depends_on('py-funcsigs@1.0.2:', type=('build', 'run'))
    depends_on('py-mccabe@0.6.1:', type=('build', 'run'))
    depends_on('py-more-itertools@4.3.0:', type=('build', 'run'))
    depends_on('py-pathlib2@2.3.2:', type=('build', 'run'))
    depends_on('py-pluggy@0.8.0:', type=('build', 'run'))
    depends_on('py-py@1.7.0:', type=('build', 'run'))
    depends_on('py-pycodestyle@2.4.0:', type=('build', 'run'))
    depends_on('py-pyflakes@2.0.0:', type=('build', 'run'))
    depends_on('py-pytest@4.0.1:', type=('build', 'run'))
    depends_on('py-pytest-cov@2.6.0:', type=('build', 'run'))
    depends_on('py-scandir@1.9.0:', type=('build', 'run'))
    depends_on('py-six@1.11.0:', type=('build', 'run'))
