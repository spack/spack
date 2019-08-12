# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLazyProperty(PythonPackage):
    """A package for making properties lazy"""

    homepage = "https://github.com/jackmaney/lazy-property"
    url      = "https://github.com/jackmaney/lazy-property/archive/0.0.1.tar.gz"

    version('0.0.1', '7e046c2441abe1bd272d5360827237b3')
    version('0.0.0', 'fda622b7f1c46ee72ad25f5e88c928f5')

    depends_on('py-setuptools', type='build')
