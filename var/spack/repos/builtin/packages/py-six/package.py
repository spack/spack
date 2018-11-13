# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySix(PythonPackage):
    """Python 2 and 3 compatibility utilities."""

    homepage = "https://pypi.python.org/pypi/six"
    url      = "https://pypi.io/packages/source/s/six/six-1.11.0.tar.gz"

    import_modules = ['six']

    version('1.11.0', 'd12789f9baf7e9fb2524c0c64f1773f8')
    version('1.10.0', '34eed507548117b2ab523ab14b2f8b55')
    version('1.9.0',  '476881ef4012262dfc8adc645ee786c4')
    version('1.8.0',  '1626eb24cc889110c38f7e786ec69885')

    extends('python', ignore=r'bin/pytest')

    # Newer versions of setuptools require six. Although setuptools is an
    # optional dependency of six, if it is not found, setup.py will fallback
    # on distutils.core instead. Don't add a setuptools dependency or we
    # won't be able to bootstrap setuptools.

    # depends_on('py-setuptools', type='build')
