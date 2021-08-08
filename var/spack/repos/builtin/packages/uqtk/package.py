# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Uqtk(CMakePackage):
    """Sandia Uncertainty Quantification Toolkit. The UQ Toolkit (UQTk) is a
    collection of libraries and tools for the quantification of uncertainty
    in numerical model predictions"""

    homepage = "https://www.sandia.gov/UQToolkit/"
    url      = "https://github.com/sandialabs/UQTk/archive/v3.0.4.tar.gz"
    git      = "https://github.com/sandialabs/UQTk.git"

    version('master', branch='master')
    version('3.1.0', sha256='56ecd3d13bdd908d568e9560dc52cc0f66d7bdcdbe64ab2dd0147a7cf1734f97')
    version('3.0.4', sha256='0a72856438134bb571fd328d1d30ce3d0d7aead32eda9b7fb6e436a27d546d2e')

    variant('pyuqtk', default=True,
            description='Compile Python scripts and interface to C++ libraries')

    depends_on('expat')
    depends_on('sundials', when='@3.1.0:')
    depends_on('blas', when='@3.1.0:')
    depends_on('lapack', when='@3.1.0:')

    extends('python', when='+pyuqtk')
    depends_on('py-numpy', when='+pyuqtk')
    depends_on('py-scipy', when='+pyuqtk')
    depends_on('py-matplotlib', when='+pyuqtk')
    depends_on('py-pymc3', when='+pyuqtk')
    depends_on('swig', when='+pyuqtk')

    # Modify the process of directly specifying blas/lapack
    # as the library name.
    patch('remove_unique_libname.patch', when='@3.1.0:')

    # Do not link the gfortran library when using the Fujitsu compiler.
    patch('not_link_gfortran.patch', when='@3.1.0:%fj')

    @when('@3.1.0:')
    def cmake_args(self):
        spec = self.spec

        # Make sure we use Spack's blas/lapack:
        lapack_libs = spec['lapack'].libs.joined(';')
        blas_libs = spec['blas'].libs.joined(';')

        args = [
            '-DCMAKE_SUNDIALS_DIR={0}'.format(spec['sundials'].prefix),
            '-DLAPACK_LIBRARIES={0}'.format(lapack_libs),
            '-DBLAS_LIBRARIES={0}'.format(blas_libs),
        ]

        if self.spec.variants['pyuqtk'].value:
            args.extend(['-DPyUQTk=ON'])

        return args

    def setup_run_environment(self, env):
        if self.spec.variants['pyuqtk'].value:
            env.prepend_path('PYTHONPATH', self.prefix)
            env.prepend_path('PYTHONPATH', '{0}/PyUQTk'.format(self.prefix))
            env.prepend_path('LD_LIBRARY_PATH', '{0}/PyUQTk/'.format(self.prefix))
            env.set('UQTK_SRC', self.prefix)
            env.set('UQTK_INS', self.prefix)
