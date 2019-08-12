# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyZopeInterface(PythonPackage):
    """This package provides an implementation of "object interfaces" for
    Python. Interfaces are a mechanism for labeling objects as conforming to a
    given API or contract. So, this package can be considered as implementation
    of the Design By Contract methodology support in Python."""

    homepage = "https://github.com/zopefoundation/zope.interface"
    url      = "https://pypi.io/packages/source/z/zope.interface/zope.interface-4.5.0.tar.gz"

    # FIXME: No idea why these import tests fail.
    # Maybe some kind of namespace issue?
    # import_modules = ['zope.interface', 'zope.interface.common']

    version('4.5.0', '7b669cd692d817772c61d2e3ad0f1e71')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
    depends_on('py-zope-event', type='test')
    depends_on('py-nose', type='test')
    depends_on('py-coverage', type='test')
