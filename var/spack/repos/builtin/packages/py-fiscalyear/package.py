# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFiscalyear(PythonPackage):
    """fiscalyear is a small, lightweight Python module providing helpful
    utilities for managing the fiscal calendar. It is designed as an extension
    of the built-in datetime and calendar modules, adding the ability to query
    the fiscal year and fiscal quarter of a date or datetime object."""

    homepage = "https://github.com/adamjstewart/fiscalyear"
    url      = "https://pypi.io/packages/source/f/fiscalyear/fiscalyear-0.1.0.tar.gz"
    git      = "https://github.com/adamjstewart/fiscalyear.git"

    maintainers = ['adamjstewart']
    import_modules = ['fiscalyear']

    version('master', branch='master')
    version('0.1.0', '30e36b259f3e72e4929abbf259335742')

    depends_on('python@2.5:')
    depends_on('py-setuptools', type='build')

    depends_on('py-pytest', type='test')
    depends_on('py-pytest-runner', type='test')
