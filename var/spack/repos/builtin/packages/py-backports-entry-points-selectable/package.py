# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBackportsEntryPointsSelectable(PythonPackage):
    """Compatibility shim providing selectable entry points for older implementations"""

    homepage = "https://github.com/jaraco/backports.entry_points_selectable"
    pypi     = "backports.entry_points_selectable/backports.entry_points_selectable-1.1.0.tar.gz"

    maintainers = ['iarspider']

    version('1.1.0', sha256='988468260ec1c196dab6ae1149260e2f5472c9110334e5d51adcb77867361f6a')

    depends_on('python@2.7.0:2.7,3.0:3.10', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-importlib-metadata@:3.8', type='build')
