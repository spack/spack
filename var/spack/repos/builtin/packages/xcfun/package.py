# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xcfun(CMakePackage):
    """Exchange-Correlation functionals with arbitrary order derivatives."""

    homepage = "https://github.com/dftlibs/xcfun"
    url = "https://github.com/dftlibs/xcfun/archive/v2.0.0a4.tar.gz"

    maintainers = ['robertodr', 'bast']

    version('2.0.0a6',
            sha256='a51086490890393439f98c5e3e4e1622908fe934bbc5063b1d4363cc4c15496d')

    extends('python')
    depends_on('cmake@3.11:', type='build')
    depends_on('python@3:')
    depends_on('py-pybind11')
    depends_on('py-numpy')

    def cmake_args(self):
        spec = self.spec

        args = [
            "-DCMAKE_INSTALL_LIBDIR=lib",
            "-DPYMOD_INSTALL_LIBDIR=/python{0}/site-packages".format(
                spec["python"].version[:-1]),
            "-DXCFUN_MAX_ORDER=8",
            "-DXCFUN_PYTHON_INTERFACE=ON",
            "-DPYTHON_EXECUTABLE={0}".format(spec['python'].command),
        ]
        return args
