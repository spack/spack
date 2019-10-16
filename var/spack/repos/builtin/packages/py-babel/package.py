# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBabel(PythonPackage):
    """Babel is an integrated collection of utilities that assist in
    internationalizing and localizing Python applications, with an
    emphasis on web-based applications."""

    homepage = "http://babel.pocoo.org/en/latest/"
    url      = "https://pypi.io/packages/source/B/Babel/Babel-2.4.0.tar.gz"

    import_modules = ['babel', 'babel.localtime', 'babel.messages']

    version('2.6.0', sha256='8cba50f48c529ca3fa18cf81fa9403be176d374ac4d60738b839122dfaaa3d23')
    version('2.4.0', sha256='8c98f5e5f8f5f088571f2c6bd88d530e331cbbcb95a7311a0db69d3dca7ec563')
    version('2.3.4', sha256='c535c4403802f6eb38173cd4863e419e2274921a01a8aad8a5b497c131c62875')

    depends_on('py-setuptools', type='build')
    depends_on('py-pytz',       type=('build', 'run'))
