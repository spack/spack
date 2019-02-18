# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyparsing(PythonPackage):
    """A Python Parsing Module."""
    homepage = "http://pyparsing.wikispaces.com/"
    url      = "https://pypi.io/packages/source/p/pyparsing/pyparsing-2.2.0.tar.gz"

    import_modules = ['pyparsing']

    version('2.2.0',  '0214e42d63af850256962b6744c948d9')
    version('2.1.10', '065908b92904e0d3634eb156f44cc80e')
    version('2.0.3',  '0fe479be09fc2cf005f753d3acc35939')

    patch('setuptools-import.patch', when='@:2.1.10')

    # Newer versions of setuptools require pyparsing. Although setuptools is an
    # optional dependency of pyparsing, if it is not found, setup.py will
    # fallback on distutils.core instead. Don't add a setuptools dependency
    # or we won't be able to bootstrap setuptools.

    # depends_on('py-setuptools', type='build')
