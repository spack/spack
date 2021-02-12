# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOwslib(PythonPackage):
    """OWSLib is a Python package for client programming with Open Geospatial
    Consortium (OGC) web service (hence OWS) interface standards, and their
    related content models."""

    homepage = "http://http://geopython.github.io/OWSLib/#installation"
    pypi = "OWSLib/OWSLib-0.16.0.tar.gz"

    version('0.23.0', sha256='0a03a9978673f377df45107024e2aae006f85afe7ef7bf4640ef663167a4386f')
    version('0.22.0', sha256='23e19ca6b8c6dfe8c9a11387818cd0440d0ccf0c71f0fe4afd210ef63f2c386f')
    version('0.21.0', sha256='408d40b3a6a210bcb3f3609b607960eeedaa63ffd574dde7896906691c354814')
    version('0.20.0', sha256='334988857b260c8cdf1f6698d07eab61839c51acb52ee10eed1275439200a40e')
    version('0.19.2', sha256='605a742d088f1ed9c946e824d0b3be94b5256931f8b230dae63e27a52c781b6d')
    version('0.19.1', sha256='11a9d67f99fff23349ea52ae19adbf9f8a10ec521d373b83ccb8547cf3063904')
    version('0.19.0', sha256='1d499981e13a1233822e94ee30c95ddd35d11f176e854d7f0cdc30ef55f5b065')
    version('0.18.0', sha256='f5645c2f28a058a794309e0349038139f2f0e2065aa40b017d6cad5baf171705')
    version('0.17.1', sha256='b2e7fd694d3cffcee79317bad492d60c0aa887aea6916517c051c3247b33b5a5')
    version('0.16.0', sha256='ec95a5e93c145a5d84b0074b9ea27570943486552a669151140debf08a100554')

    depends_on('py-setuptools',     type='build')
    depends_on('py-python-dateutil@1.5:',  type=('build', 'run'))
    depends_on('py-pytz',           type=('build', 'run'))
    depends_on('py-requests@1.0:',  type=('build', 'run'))
    depends_on('py-pyproj',           type=('build', 'run'))
