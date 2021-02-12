# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDateparser(PythonPackage):
    """dateparser -- python parser for human readable dates"""

    homepage = "https://github.com/scrapinghub/dateparser"
    pypi = "dateparser/dateparser-0.7.2.tar.gz"

    version('1.0.0', sha256='159cc4e01a593706a15cd4e269a0b3345edf3aef8bf9278a57dac8adf5bf1e4a')
    version('0.7.6', sha256='e875efd8c57c85c2d02b238239878db59ff1971f5a823457fcc69e493bf6ebfa')
    version('0.7.5', sha256='cfa0db2df93903406ca867fd922ac4f482a5fb162356f31d2d7a3012fa5f0d14')
    version('0.7.4', sha256='fb5bfde4795fa4b179fe05c2c25b3981f785de26bec37e247dee1079c63d5689')
    version('0.7.2', sha256='e1eac8ef28de69a554d5fcdb60b172d526d61924b1a40afbbb08df459a36006b')

    variant('calendars', default=True, description='Add calendar libraries')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-python-dateutil@2.7.5:', type=('build', 'run'))
    depends_on('py-pytz', type=('build', 'run'))
    depends_on('py-regex', type=('build', 'run'))
    depends_on('py-tzlocal', type=('build', 'run'))
    depends_on('py-umalqurra', type=('build', 'run'), when='+calendars')
    depends_on('py-ruamel-yaml', type=('build', 'run'), when='+calendars')
    depends_on('py-convertdate', type=('build', 'run'), when='+calendars')
    depends_on('py-jdatetime', type=('build', 'run'), when='+calendars')
