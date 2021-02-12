# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyUvloop(PythonPackage):
    """uvloop is a fast, drop-in replacement of the built-in asyncio event"""

    homepage = "http://github.com/MagicStack/uvloop"
    pypi = "uvloop/uvloop-0.14.0.tar.gz"

    version('0.15.0', sha256='1a503d5b49da6e3dd5607d6e533a5315b1caedbf629901807c65a23a09cad065')
    version('0.14.0', sha256='123ac9c0c7dd71464f58f1b4ee0bbd81285d96cdda8bc3519281b8973e3a461e')

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
