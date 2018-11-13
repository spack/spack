# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAttrs(PythonPackage):
    """Classes Without Boilerplate"""

    homepage = "http://attrs.org/"
    url      = "https://pypi.io/packages/source/a/attrs/attrs-18.1.0.tar.gz"

    import_modules = ['attr']

    version('18.1.0', '3f3f3e0750dab74cfa1dc8b0fd7a5f86')
    version('16.3.0', '4ec003c49360853cf935113d1ae56151')

    depends_on('py-setuptools', type='build')

    depends_on('py-coverage', type='test')
    depends_on('py-hypothesis', type='test')
    depends_on('py-pympler', type='test')
    depends_on('py-pytest', type='test')
    depends_on('py-six', type='test')
    depends_on('py-zope-interface', type='test')
