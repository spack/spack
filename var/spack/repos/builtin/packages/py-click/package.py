# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyClick(PythonPackage):
    """A simple wrapper around optparse for powerful command line utilities."""

    homepage = "http://github.com/mitsuhiko/click"
    url = "https://pypi.io/packages/source/c/click/Click-7.0.tar.gz"

    version('7.0', sha256='5b94b49521f6456670fdb30cd82a4eca9412788a93fa6dd6df72c94d5a8ff2d7')
    version('6.6', sha256='cc6a19da8ebff6e7074f731447ef7e112bd23adf3de5c597cf9989f2fd8defe9',
            url='https://pypi.io/packages/source/c/click/click-6.6.tar.gz')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
