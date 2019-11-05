# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDateparser(PythonPackage):
    """dateparser -- python parser for human readable dates"""

    homepage = "https://github.com/scrapinghub/dateparser"
    url      = "https://pypi.io/packages/source/d/dateparser/dateparser-0.7.2.tar.gz"

    version('0.7.2', sha256='e1eac8ef28de69a554d5fcdb60b172d526d61924b1a40afbbb08df459a36006b')

    variant('calendars', default=True, help='Add calendar libraries')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-convertdate@2.1.3:', type=('build', 'run'), when='+calendars')
    depends_on('py-jdatetime@3.1.0:', type=('build', 'run'), when='+calendars')
    depends_on('py-python-dateutil@2.7.5:', type=('build', 'run'))
    depends_on('py-pytz@2018.9:', type=('build', 'run'))
    depends_on('py-regex@2019.01.24:', type=('build', 'run'))
    depends_on('py-tzlocal@1.5.1:', type=('build', 'run'))
    depends_on('py-umalqurra@0.2:', type=('build', 'run'), when='+calendars')
    depends_on('py-ruamel-yaml', type=('build', 'run'), when='+calendars')
    depends_on('py-mock', type='test')
    depends_on('py-nose', type='test')
    depends_on('py-parameterized', type='test')
    depends_on('py-six', type='test')
    depends_on('py-coverage', type='test')
