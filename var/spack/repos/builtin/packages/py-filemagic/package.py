# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFilemagic(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://pypi.io/packages/source/f/filemagic/filemagic-1.6.tar.gz"

    version('1.6', sha256='e684359ef40820fe406f0ebc5bf8a78f89717bdb7fed688af68082d991d6dbf3')

    depends_on('py-setuptools', type='build')
    depends_on('py-mock', type='test', when='^python@3:')
    depends_on('py-unittest2', type='test')
