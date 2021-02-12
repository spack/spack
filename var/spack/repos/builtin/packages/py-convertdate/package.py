# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyConvertdate(PythonPackage):
    """Converts between Gregorian dates and other calendar
    systems.Calendars included: Baha'i, French Republican, Hebrew,
    Indian Civil, Islamic, ISO, Julian, Mayan and Persian."""

    homepage = "https://github.com/fitnr/convertdate/"
    pypi = "convertdate/convertdate-2.2.0.tar.gz"

    version('2.3.0', sha256='1f5919e6a64a8bda46a44af2e3c20fa75bcf22c51fb63c638d36d24ef8982446')
    version('2.2.2', sha256='2fd8a44d5f39a2732f26cd481e3424cc10d56a23174c2d85783dbfb7d9dcc159')
    version('2.2.1', sha256='6ce4747423fe2dde55bbdf89f0c3dc68044176d16d5f6a2cfbfe6c68b99db405')
    version('2.2.0', sha256='9d2b0cd8d5382d2458d4cfa59665abba398a9e9bfd3a01c6f61b7b47768d28bf')

    depends_on('py-setuptools', type='build')
    depends_on('py-pytz@2014.10:2019.13', type=('build', 'run'))
    depends_on('py-pymeeus@0.3.6:1', type=('build', 'run'))
