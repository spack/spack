# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNosexcover(PythonPackage):
    """A companion to the built-in nose.plugins.cover, this plugin will write
    out an XML coverage report to a file named coverage.xml."""

    homepage = "https://github.com/cmheisel/nose-xcover"
    url = "https://pypi.io/packages/source/n/nosexcover/nosexcover-1.0.11.tar.gz"

    version('1.0.11', 'f32ef4824b4484343e9766b2c376365d')

    depends_on('py-setuptools', type='build')
    depends_on('py-nose',        type=('build', 'run'))
    depends_on('py-coverage@3.4:',        type=('build', 'run'))
