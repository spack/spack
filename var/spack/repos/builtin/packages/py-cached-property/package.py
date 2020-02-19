##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyCachedProperty(PythonPackage):
    """A decorator for caching properties in classes."""

    homepage = "https://github.com/pydanny/cached-property"
    url      = "https://github.com/pydanny/cached-property/archive/1.3.0.tar.gz"

    version('1.5.1', sha256='b8d80b92f78a147a5bcc6eb1dbf9c5b5c5a003a6d01de5a40da3479516e4e091')

    depends_on('py-setuptools', type='build')
