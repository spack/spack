# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPy2cairo(WafPackage):
    """Pycairo is a set of Python bindings for the cairo graphics library."""

    homepage = "https://www.cairographics.org/pycairo/"
    url      = "https://cairographics.org/releases/py2cairo-1.10.0.tar.bz2"

    version('1.10.0', '20337132c4ab06c1146ad384d55372c5')

    extends('python')

    depends_on('python', type=('build', 'run'))
    depends_on('cairo@1.10.0:')
    depends_on('pixman')
    depends_on('pkgconfig', type='build')

    depends_on('py-pytest', type='test')

    def installtest(self):
        with working_dir('test'):
            pytest = which('py.test')
            pytest()
