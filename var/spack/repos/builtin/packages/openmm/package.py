# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Openmm(CMakePackage, CudaPackage):
    """A high performance toolkit for molecular simulation. Use it as
    a library, or as an application. We include extensive language
    bindings for Python, C, C++, and even Fortran. The code is open
    source and actively maintained on Github, licensed under MIT and
    LGPL. Part of the Omnia suite of tools for predictive biomolecular
    simulation. """

    homepage = "http://openmm.org/"
    url      = "https://github.com/openmm/openmm/archive/7.4.1.tar.gz"

    version('7.4.1', sha256='e8102b68133e6dcf7fcf29bc76a11ea54f30af71d8a7705aec0aee957ebe3a6d')

    install_targets = ['install', 'PythonInstall']

    depends_on('python')
    depends_on('doxygen')
    depends_on('swig')
    depends_on('fftw')
    depends_on('py-cython', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    extends('python')

    def patch(self):
        install_string = "set(PYTHON_SETUP_COMMAND \"install " \
                         "--prefix={0}\")".format(self.prefix)

        filter_file(r'set\(PYTHON_SETUP_COMMAND \"install.*',
                    install_string,
                    'wrappers/python/CMakeLists.txt')
