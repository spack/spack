# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyConvertdate(PythonPackage):
    """The convertdate package was originally developed as "Python Date
    Utils" by Phil Schwartz. It had been significantly updated and expanded."""

    homepage = "https://github.com/fitnr/convertdate/"
    url      = "https://pypi.io/packages/source/c/convertdate/convertdate-2.2.0.tar.gz"

    version('2.2.0', sha256='9d2b0cd8d5382d2458d4cfa59665abba398a9e9bfd3a01c6f61b7b47768d28bf')

    depends_on('py-setuptools', type='build')
    depends_on('py-pytz@2014.10:2019.13', type=('build', 'run'))
    depends_on('py-pymeeus@0.3.6:1', type=('build', 'run'))
