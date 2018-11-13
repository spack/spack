# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOpenslidePython(PythonPackage):
    """OpenSlide Python is a Python interface to the OpenSlide library."""

    homepage = "https://github.com/openslide/openslide-python"
    url      = "https://github.com/openslide/openslide-python/archive/v1.1.1.tar.gz"

    version('1.1.1', '8c207e48069887b63ea1c7bc9eb7dfc0')

    import_modules = ['openslide']

    depends_on('openslide@3.4.0:')
    depends_on('python@2.6:2.8,3.3:')
    depends_on('py-setuptools', type='build')
    depends_on('py-pillow+jpeg+jpeg2000+tiff', type=('build', 'run'))
