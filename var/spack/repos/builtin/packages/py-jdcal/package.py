# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJdcal(PythonPackage):
    """Julian dates from proleptic Gregorian and Julian calendars"""

    homepage = "http://github.com/phn/jdcal"
    url      = "https://pypi.io/packages/source/j/jdcal/jdcal-1.3.tar.gz"

    version('1.3', '885ba61d28992f26acffec131bd2a17e')
    version('1.2', 'ab8d5ba300fd1eb01514f363d19b1eb9')

    depends_on('py-setuptools', type='build')
