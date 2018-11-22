# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyClickPlugins(PythonPackage):
    """An extension module for py-click to register external CLI
       commands via setuptools entry-points."""

    homepage = "https://pypi.org/project/click-plugins/"
    url      = "https://pypi.io/packages/source/c/click-plugins/click-plugins-1.0.4.tar.gz"

    version('1.0.4', '3db73ba58271e3d9644be9b9c03a9d8d')

    depends_on('py-setuptools', type='build')
    depends_on('py-click@3.0:', type=('build', 'run'))
