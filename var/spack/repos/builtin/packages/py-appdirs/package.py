# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAppdirs(PythonPackage):
    """A small Python module for determining appropriate platform-specific
    dirs, e.g. a "user data dir"."""

    homepage = "https://github.com/ActiveState/appdirs"
    url      = "https://pypi.io/packages/source/a/appdirs/appdirs-1.4.3.tar.gz"

    import_modules = ['appdirs']

    version('1.4.3', '44c679904082a2133f5566c8a0d3ab42')
    version('1.4.0', '1d17b4c9694ab84794e228f28dc3275b')

    patch('setuptools-import.patch', when='@:1.4.0')

    # Newer versions of setuptools require appdirs. Although setuptools is an
    # optional dependency of appdirs, if it is not found, setup.py will
    # fallback on distutils.core instead. Don't add a setuptools dependency
    # or we won't be able to bootstrap setuptools.

    # depends_on('py-setuptools', type='build')
