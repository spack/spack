# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIso8601(PythonPackage):
    """Simple module to parse ISO 8601 dates"""

    homepage = "https://pyiso8601.readthedocs.io/en/latest/"
    pypi     = "iso8601/iso8601-0.1.14.tar.gz"

    version('0.1.14', sha256='8aafd56fa0290496c5edbb13c311f78fa3a241f0853540da09d9363eae3ebd79')

    depends_on('py-setuptools', type='build')
