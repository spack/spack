# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIsodate(PythonPackage):
    """ISO 8601 date/time parser."""

    homepage = "https://github.com/gweis/isodate"
    url      = "https://pypi.io/packages/source/i/isodate/isodate-0.6.0.tar.gz"

    version('0.6.0', sha256='2e364a3d5759479cdb2d37cce6b9376ea504db2ff90252a2e5b7cc89cc9ff2d8')

    depends_on('py-setuptools', type='build')

    depends_on('py-six', type='run')
