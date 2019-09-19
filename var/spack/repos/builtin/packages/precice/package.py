# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Precice(CMakePackage):
    """preCICE (Precise Code Interaction Coupling Environment) is a
    coupling library for partitioned multi-physics simulations.
    Partitioned means that preCICE couples existing programs (solvers)
    capable of simulating a subpart of the complete physics involved in
    a simulation."""

    homepage = 'https://www.precice.org'
    git      = 'https://github.com/precice/precice.git'
    url      = 'https://github.com/precice/precice/archive/v1.2.0.tar.gz'
    maintainers = ['fsimonis', 'MakisH']

    version('develop', branch='develop')
    version('1.6.1', sha256='7d0c54faa2c69e52304f36608d93c408629868f16f3201f663a0f9b2008f0763')
    version('1.6.0', sha256='c3b16376fda9eb3449adb6cc3c1e267c3dc792a5d118e37d93a32a59b5a4bc6f')
    version('1.5.2', sha256='051e0d7655a91f8681901e5c92812e48f33a5779309e2f104c99f5a687e1a418')
    version('1.5.1', sha256='fbe151f1a9accf9154362c70d15254935d4f594d189982c3a99fdb3dd9d9e665')
    version('1.5.0', sha256='a2a794becd08717e3049252134ae35692fed71966ed32e22cca796a169c16c3e')
    version('1.4.1', sha256='dde4882edde17882340f9f601941d110d5976340bd71af54c6e6ea22ae56f1a5')
    version('1.4.0', sha256='3499bfc0941fb9f004d5e32eb63d64f93e17b4057fab3ada1cde40c8311bd466')
    version('1.3.0', sha256='610322ba1b03df8e8f7d060d57a6a5afeabd5db4e8c4a638d04ba4060a3aec96')
    version('1.2.0', sha256='0784ecd002092949835151b90393beb6e9e7a3e9bd78ffd40d18302d6da4b05b')
    # Skip version 1.1.1 entirely, the cmake was lacking install.

    variant('mpi', default=True, description='Enable MPI support')
    variant('petsc', default=False, description='Enable PETSc support')
    variant('python', default=False, description='Enable Python support')
    variant('shared', default=True, description='Build shared libraries')

    depends_on('cmake@3.5:', type='build')
    depends_on('cmake@3.10.2:', type='build', when='@1.4:')
    depends_on('boost@1.60.0:')
    depends_on('boost@1.65.1:', when='@1.4:')
    depends_on('eigen@3.2:')
    depends_on('eigen@:3.3.7', type='build', when='@:1.5')  # bug in prettyprint
    depends_on('libxml2')
    depends_on('mpi', when='+mpi')
    depends_on('petsc@3.6:', when='+petsc')
    depends_on('python@2.7:2.8', when='+python', type=('build', 'run'))
    # numpy 1.17+ requires Python 3
    depends_on('py-numpy@:1.16', when='+python', type=('build', 'run'))

    def cmake_args(self):
        """Populate cmake arguments for precice."""
        spec = self.spec

        # The xSDK installation policies were implemented after 1.5.2
        xsdk_mode = spec.satisfies("@1.6:")

        def variant_bool(feature, on='ON', off='OFF'):
            """Ternary for spec variant to ON/OFF string"""
            if feature in spec:
                return on
            return off

        cmake_args = [
            '-DBUILD_SHARED_LIBS:BOOL=%s' % variant_bool('+shared'),
            '-DMPI:BOOL=%s' % variant_bool('+mpi'),
        ]

        # Boost
        if xsdk_mode:
            cmake_args.append('-DTPL_ENABLE_BOOST=ON')
        cmake_args.append('-DBOOST_ROOT=%s' % spec['boost'].prefix)

        # Eigen3
        if xsdk_mode:
            cmake_args.append('-DTPL_ENABLE_EIGEN3=ON')
        cmake_args.append(
            '-DEIGEN3_INCLUDE_DIR=%s' % spec['eigen'].headers.directories[0])

        # LibXML2
        if xsdk_mode:
            cmake_args.append('-DTPL_ENABLE_LIBXML2=ON')
        libxml2_includes = spec['libxml2'].headers.directories[0]
        cmake_args.extend([
            '-DLIBXML2_INCLUDE_DIRS=%s' % libxml2_includes,
            '-DLIBXML2_LIBRARIES=%s' % spec['libxml2'].libs[0],
        ])

        # PETSc
        if '+petsc' in spec:
            cmake_args.extend([
                '-DTPL_ENABLE_PETSC:BOOL=ON' if xsdk_mode else '-DPETSC=ON',
                '-DPETSC_DIR=%s' % spec['petsc'].prefix,
                '-DPETSC_ARCH=.'
            ])
        else:
            cmake_args.append('-DPETSC:BOOL=OFF')

        # Python
        if '+python' in spec:
            python_library = spec['python'].libs[0]
            python_include = spec['python'].headers.directories[0]
            numpy_include = join_path(
                spec['py-numpy'].prefix,
                spec['python'].package.site_packages_dir,
                'numpy', 'core', 'include')
            cmake_args.extend([
                '-DTPL_ENABLE_PYTHON:BOOL=ON' if xsdk_mode else '-DPYTHON=ON',
                '-DPYTHON_INCLUDE_DIR=%s' % python_include,
                '-DNumPy_INCLUDE_DIR=%s' % numpy_include,
                '-DPYTHON_LIBRARY=%s' % python_library
            ])
        else:
            cmake_args.append('-DPYTHON:BOOL=OFF')

        return cmake_args
