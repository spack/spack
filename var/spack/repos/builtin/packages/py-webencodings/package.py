# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWebencodings(PythonPackage):
    """This is a Python implementation of the WHATWG Encoding standard."""

    homepage = "https://github.com/gsnedders/python-webencodings"
    url      = "https://pypi.io/packages/source/w/webencodings/webencodings-0.5.1.tar.gz"

    version('0.5.1', '32f6e261d52e57bf7e1c4d41546d15b8')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.6:2.8,3.3:',        type=('build', 'run'))
