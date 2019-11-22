# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCachedProperty(PythonPackage):
    """A decorator for caching properties in classes."""

    homepage = "https://pypi.org/project/cached-property/"
    url      = "https://pypi.io/packages/source/c/cached-property/cached-property-1.5.1.tar.gz"

    version('1.5.1', '4b6f3cd429da5f487f4ebf3242bb991f')

    depends_on('py-setuptools', type='build')
