# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os.path

from spack import *


class QuantumEspresso(Package):
    """Quantum-ESPRESSO is an integrated suite of Open-Source computer codes
    for electronic-structure calculations and materials modeling at the
    nanoscale. It is based on density-functional theory, plane waves, and
    pseudopotentials.
    """

    homepage = 'http://quantum-espresso.org'
    url      = 'https://github.com/QEF/q-e/archive/qe-6.2.0.tar.gz'

    version('6.2.0', '972176a58d16ae8cf0c9a308479e2b97')
    version('6.1.0', '3fe861dcb5f6ec3d15f802319d5d801b')
    version('5.4',   '085f7e4de0952e266957bbc79563c54e')
    version('5.3',   'be3f8778e302cffb89258a5f936a7592')

    variant('mpi', default=True, description='Builds with mpi support')
    variant('openmp', default=False, description='Enables openMP support')
    variant('scalapack', default=True, description='Enables scalapack support')
    variant('elpa', default=True, description='Uses elpa as an eigenvalue solver')

    # Support for HDF5 has been added starting in version 6.1.0 and is
    # still experimental, therefore we default to False for the variant
    variant('hdf5', default=False, description='Builds with HDF5 support')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+mpi')
    depends_on('scalapack', when='+scalapack+mpi')

    depends_on('fftw+mpi', when='+mpi')
    depends_on('fftw~mpi', when='~mpi')
    depends_on('elpa+openmp', when='+elpa+openmp')
    depends_on('elpa~openmp', when='+elpa~openmp')
    depends_on('hdf5', when='+hdf5')

    patch('dspev_drv_elpa.patch', when='@6.1.0:+elpa ^elpa@2016.05.004')
    patch('dspev_drv_elpa.patch', when='@6.1.0:+elpa ^elpa@2016.05.003')

    # We can't ask for scalapack or elpa if we don't want MPI
    conflicts(
        '+scalapack',
        when='~mpi',
        msg='scalapack is a parallel library and needs MPI support'
    )

    conflicts(
        '+elpa',
        when='~mpi',
        msg='elpa is a parallel library and needs MPI support'
    )

    # Elpa is formally supported by @:5.4.0, but QE configure searches
    # for it in the wrong folders (or tries to download it within
    # the build directory). Instead of patching Elpa to provide the
    # folder QE expects as a link, we issue a conflict here.
    conflicts('+elpa', when='@:5.4.0')
    conflicts('+hdf5', when='@:5.4.0')

    # Spurious problems running in parallel the Makefile
    # generated by the configure
    parallel = False

    def install(self, spec, prefix):

        prefix_path = prefix.bin if '@:5.4.0' in spec else prefix
        options = ['-prefix={0}'.format(prefix_path)]

        if '+mpi' in spec:
            options.append('--enable-parallel=yes')
        else:
            options.append('--enable-parallel=no')

        if '+openmp' in spec:
            options.append('--enable-openmp')

        if '+scalapack' in spec:
            scalapack_option = 'intel' if '^intel-mkl' in spec else 'yes'
            options.append('--with-scalapack={0}'.format(scalapack_option))

        if '+elpa' in spec:

            # Spec for elpa
            elpa = spec['elpa']

            # Find where the Fortran module resides
            elpa_module = find(elpa.prefix, 'elpa.mod')

            # Compute the include directory from there: versions
            # of espresso prior to 6.1 requires -I in front of the directory
            elpa_include = '' if '@6.1:' in spec else '-I'
            elpa_include += os.path.dirname(elpa_module[0])

            options.extend([
                '--with-elpa-include={0}'.format(elpa_include),
                '--with-elpa-lib={0}'.format(elpa.libs[0])
            ])

        if '+hdf5' in spec:
            options.append('--with-hdf5={0}'.format(spec['hdf5'].prefix))

        # Add a list of directories to search
        search_list = []
        for dependency_spec in spec.dependencies():
            search_list.extend([
                dependency_spec.prefix.lib,
                dependency_spec.prefix.lib64
            ])

        search_list = " ".join(search_list)

        options.extend([
            'LIBDIRS={0}'.format(search_list),
            'F90={0}'.format(env['SPACK_FC']),
            'CC={0}'.format(env['SPACK_CC'])
        ])

        configure(*options)

        # Apparently the build system of QE is so broken that:
        #
        # 1. The variable reported on stdout as HDF5_LIBS is actually
        #    called HDF5_LIB (singular)
        # 2. The link flags omit a few `-L` from the line, and this
        #    causes the linker to break
        #
        # Below we try to match the entire HDF5_LIB line and substitute
        # with the list of libraries that needs to be linked.
        if '+hdf5' in spec:
            make_inc = join_path(self.stage.source_path, 'make.inc')
            hdf5_libs = ' '.join(spec['hdf5:hl,fortran'].libs)
            filter_file(
                'HDF5_LIB([\s]*)=([\s\w\-\/.,]*)',
                'HDF5_LIB = {0}'.format(hdf5_libs),
                make_inc
            )

        make('all')

        if 'platform=darwin' in spec:
            mkdirp(prefix.bin)
            for filename in glob.glob("bin/*.x"):
                install(filename, prefix.bin)
        else:
            make('install')
