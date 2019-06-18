# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIsodate(PythonPackage):
    """ISO 8601 date/time parser."""

    homepage = "https://github.com/gweis/isodate"
    url      = "https://pypi.io/packages/source/i/isodate/isodate-0.6.0.tar.gz"

    version('0.6.0', '0e1203fce27ce65e2d01c5f21c4d428f')

    depends_on('py-setuptools', type='build')

    depends_on('py-six', type='run')
