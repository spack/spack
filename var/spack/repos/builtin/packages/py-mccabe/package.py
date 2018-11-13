# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMccabe(PythonPackage):
    """Ned's script to check McCabe complexity."""

    homepage = "https://github.com/PyCQA/mccabe"
    url      = "https://github.com/PyCQA/mccabe/archive/0.5.2.tar.gz"

    version('0.6.1', '0360af86f0bce7a839bd3cba517edf9c')
    version('0.6.0', '38f46ff70b5d2c02155f8fd4d96fb791')
    version('0.5.3', 'a75f57079ce10556fd3c63a5f6b4d706')
    version('0.5.2', '3cdf2d7faa1464b18905fe9a7063a632')
    version('0.5.1', '864b364829156701bec797712be8ece0')
    version('0.5.0', '71c0ce5e5c4676753525154f6c5d3af8')
    version('0.4.0', '9cf5712e5f1785aaa27273a4328babe4')
    version('0.3.1', '45c48c0978e6fc1f31fedcb918178abb')
    version('0.3',   'c583f58ea28be12842c001473d77504d')
    version('0.2.1', 'fcba311ebd999f48359a8ab28da94b30')
    version('0.2',   '36d4808c37e187dbb1fe2373a0ac6645')
    version('0.1',   '3c9e8e72612a9c01d865630cc569150a')

    depends_on('python@2.7:2.8,3.3:')

    depends_on('py-setuptools', type='build')
    depends_on('py-pytest', type='test')

    def patch(self):
        """Filter pytest-runner requirement out of setup.py."""
        filter_file("['pytest-runner']", "[]", 'setup.py', string=True)
