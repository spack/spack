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

    version('2.6.0', 'c384ac03026e8fe6f9b90f55201f1bff')
    version('2.4.0', '90e7a0add19b2036a9b415630a0d9388')
    version('2.3.4', 'afa20bc55b0e991833030129ad498f35')

    depends_on('py-setuptools', type='build')
    depends_on('py-pytz',       type=('build', 'run'))
