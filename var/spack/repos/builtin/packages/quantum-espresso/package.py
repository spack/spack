# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    url = 'https://gitlab.com/QEF/q-e/-/archive/qe-6.4.1/q-e-qe-6.4.1.tar.gz'
    git = 'https://gitlab.com/QEF/q-e.git'

    version('develop', branch='develop')
    version('6.4.1', sha256='b0d7e9f617b848753ad923d8c6ca5490d5d82495f82b032b71a0ff2f2e9cfa08')
    version('6.4', sha256='781366d03da75516fdcf9100a1caadb26ccdd1dedd942a6f8595ff0edca74bfe')
    version('6.3',   '1b67687d90d1d16781d566d44d14634c')
    version('6.2.1', '769cc973382156bffd35254c3dbaf453')
    version('6.2.0', '972176a58d16ae8cf0c9a308479e2b97')
    version('6.1.0', '3fe861dcb5f6ec3d15f802319d5d801b')
    version('6.0.0', 'd915f2faf69d0e499f8e1681c42cbfc9')
    version('5.4',   '085f7e4de0952e266957bbc79563c54e')
    version('5.3',   'be3f8778e302cffb89258a5f936a7592')

    variant('mpi', default=True, description='Builds with mpi support')
    variant('openmp', default=False, description='Enables openMP support')
    variant('scalapack', default=True, description='Enables scalapack support')
    variant('elpa', default=False, description='Uses elpa as an eigenvalue solver')

    # Support for HDF5 has been added starting in version 6.1.0 and is
    # still experimental, therefore we default to False for the variant
    variant(
        'hdf5', default='none', description='Builds with HDF5 support',
        values=('parallel', 'serial', 'none'), multi=False
    )

    # Enables building Electron-phonon Wannier 'epw.x' executable
    # http://epw.org.uk/Main/About
    variant('epw', default=False,
            description='Builds Electron-phonon Wannier executable')

    # Dependencies
    depends_on('blas')
    depends_on('lapack')
    depends_on('fftw-api@3')
    depends_on('mpi', when='+mpi')
    depends_on('scalapack', when='+scalapack+mpi')
    depends_on('elpa+openmp', when='+elpa+openmp')
    depends_on('elpa~openmp', when='+elpa~openmp')
    # Versions of HDF5 prior to 1.8.16 lead to QE runtime errors
    depends_on('hdf5@1.8.16:+fortran+hl+mpi', when='hdf5=parallel')
    depends_on('hdf5@1.8.16:+fortran+hl~mpi', when='hdf5=serial')

    # TODO: enable building EPW when ~mpi
    depends_on('mpi', when='+epw')

    patch('dspev_drv_elpa.patch', when='@6.1.0:+elpa ^elpa@2016.05.004')
    patch('dspev_drv_elpa.patch', when='@6.1.0:+elpa ^elpa@2016.05.003')

    # Conflicts
    # MKL with 64-bit integers not supported.
    conflicts(
        '^intel-mkl+ilp64',
        msg='Quantum ESPRESSO does not support MKL 64-bit integer variant'
    )

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

    # HDF5 support introduced in 6.1
    hdf5_warning = 'HDF5 support only in QE 6.1 and later'
    conflicts('hdf5=parallel', when='@:6.0', msg=hdf5_warning)
    conflicts('hdf5=serial', when='@:6.0', msg=hdf5_warning)

    conflicts(
        'hdf5=parallel',
        when='~mpi',
        msg='parallel HDF5 requires MPI support'
    )

    conflicts(
        'hdf5=serial',
        when='~mpi @6.1:6.3',
        msg='serial HDF5 in serial QE only works in develop version'
    )

    # Elpa is formally supported by @:5.4.0, but QE configure searches
    # for it in the wrong folders (or tries to download it within
    # the build directory). Instead of patching Elpa to provide the
    # folder QE expects as a link, we issue a conflict here.
    conflicts('+elpa', when='@:5.4.0')

    # The first version of Q-E to feature integrated EPW is 6.0.0,
    # as per http://epw.org.uk/Main/DownloadAndInstall .
    # Complain if trying to install a version older than this.
    conflicts('+epw', when='@:5',
              msg='EPW only available from version 6.0.0 and on')

    # Below goes some constraints as shown in the link above.
    # Constraints may be relaxed as successful reports
    # of different compiler+mpi combinations arrive

    # TODO: enable building EPW when ~mpi
    conflicts('+epw', when='~mpi', msg='EPW needs MPI')

    # EPW doesn't gets along well with OpenMPI 2.x.x
    conflicts('+epw', when='^openmpi@2.0.0:2.999.999',
              msg='OpenMPI version incompatible with EPW')

    # EPW also doesn't gets along well with PGI 17.x + OpenMPI 1.10.7
    conflicts('+epw', when='^openmpi@1.10.7%pgi@17.0:17.12',
              msg='PGI+OpenMPI version combo incompatible with EPW')

    # Spurious problems running in parallel the Makefile
    # generated by the configure
    parallel = False

    # QE upstream patches
    # QE 6.3 requires multiple patches to fix MKL detection
    # There may still be problems on Mac with MKL detection
    patch_url = 'https://gitlab.com/QEF/q-e/commit/0796e1b7c55c9361ecb6515a0979280e78865e36.diff'
    patch_checksum = 'bc8c5b8523156cee002d97dab42a5976dffae20605da485a427b902a236d7e6b'
    patch(patch_url, sha256=patch_checksum, when='@6.3:6.3.0')

    # QE 6.3 `make install` broken and a patch must be applied
    patch_url = 'https://gitlab.com/QEF/q-e/commit/88e6558646dbbcfcafa5f3fa758217f6062ab91c.diff'
    patch_checksum = 'b776890d008e16cca28c31299c62f47de0ba606b900b17cbc27c041f45e564ca'
    patch(patch_url, sha256=patch_checksum, when='@6.3:6.3.0')

    def install(self, spec, prefix):

        prefix_path = prefix.bin if '@:5.4.0' in spec else prefix
        options = ['-prefix={0}'.format(prefix_path)]

        # QE autoconf compiler variables has some limitations:
        # 1. There is no explicit MPICC variable so we must re-purpose
        #    CC for the case of MPI.
        # 2. F90 variable is set to be consistent with MPIF90 wrapper
        # 3. If an absolute path for F90 is set, the build system breaks.
        #
        # Thus, due to 2. and 3. the F90 variable is not explictly set
        # because it would be mostly pointless and could lead to erroneous
        # behaviour.
        if '+mpi' in spec:
            mpi = spec['mpi']
            options.append('--enable-parallel=yes')
            options.append('MPIF90={0}'.format(mpi.mpifc))
            options.append('CC={0}'.format(mpi.mpicc))
        else:
            options.append('--enable-parallel=no')
            options.append('CC={0}'.format(env['SPACK_CC']))

        options.append('F77={0}'.format(env['SPACK_F77']))
        options.append('F90={0}'.format(env['SPACK_FC']))

        if '+openmp' in spec:
            options.append('--enable-openmp')

        # QE external BLAS, FFT, SCALAPACK detection is a bit tricky.
        # More predictable to pass in the correct link line to QE.
        # If external detection of BLAS, LAPACK and FFT fails, QE
        # is supposed to revert to internal versions of these libraries
        # instead -- but more likely it will pickup versions of these
        # libraries found in its the system path, e.g. Red Hat or
        # Ubuntu's FFTW3 package.

        # FFT
        # FFT detection gets derailed if you pass into the CPPFLAGS, instead
        # you need to pass it in the FFTW_INCLUDE and FFT_LIBS directory.
        # QE supports an internal FFTW2, but only an external FFTW3 interface.

        if '^intel-mkl' in spec:
            # A seperate FFT library is not needed when linking against MKL
            options.append(
                'FFTW_INCLUDE={0}'.format(join_path(env['MKLROOT'],
                                                    'include/fftw')))
        if '^fftw@3:' in spec:
            fftw_prefix = spec['fftw'].prefix
            options.append('FFTW_INCLUDE={0}'.format(fftw_prefix.include))
            fftw_ld_flags = spec['fftw'].libs.ld_flags
            options.append('FFT_LIBS={0}'.format(fftw_ld_flags))

        # External BLAS and LAPACK requires the correct link line into
        # BLAS_LIBS, do no use LAPACK_LIBS as the autoconf scripts indicate
        # that this variable is largely ignored/obsolete.

        # For many Spack packages, lapack.libs = blas.libs, hence it will
        # appear twice in in link line but this is harmless
        lapack_blas = spec['lapack'].libs + spec['blas'].libs

        options.append('BLAS_LIBS={0}'.format(lapack_blas.ld_flags))

        if '+scalapack' in spec:
            scalapack_option = 'intel' if '^intel-mkl' in spec else 'yes'
            options.append('--with-scalapack={0}'.format(scalapack_option))

        if '+elpa' in spec:

            # Spec for elpa
            elpa = spec['elpa']

            # Compute the include directory from there: versions
            # of espresso prior to 6.1 requires -I in front of the directory
            elpa_include = '' if '@6.1:' in spec else '-I'
            elpa_include += os.path.join(
                elpa.headers.directories[0],
                'modules'
            )

            options.extend([
                '--with-elpa-include={0}'.format(elpa_include),
                '--with-elpa-lib={0}'.format(elpa.libs[0])
            ])

        if spec.variants['hdf5'].value != 'none':
            options.append('--with-hdf5={0}'.format(spec['hdf5'].prefix))

        configure(*options)

        # Apparently the build system of QE is so broken that
        # make_inc needs to be modified manually:
        #
        # 1. The variable reported on stdout as HDF5_LIBS is actually
        #    called HDF5_LIB (singular)
        # 2. The link flags omit a few `-L` from the line, and this
        #    causes the linker to break
        # 3. Serial HDF5 case is supported both with and without MPI.
        #
        # Below we try to match the entire HDF5_LIB line and substitute
        # with the list of libraries that needs to be linked.
        if spec.variants['hdf5'].value != 'none':
            make_inc = join_path(self.stage.source_path, 'make.inc')
            hdf5_libs = ' '.join(spec['hdf5:hl,fortran'].libs)
            filter_file(r'HDF5_LIB([\s]*)=([\s\w\-\/.,]*)',
                        'HDF5_LIB = {0}'.format(hdf5_libs),
                        make_inc)
            if spec.variants['hdf5'].value == 'serial':
                # Note that there is a benign side effect with this filter
                # file statement. It replaces an instance of MANUAL_DFLAGS
                # that is a comment in make.inc.
                filter_file(r'MANUAL_DFLAGS([\s]*)=([\s]*)',
                            'MANUAL_DFLAGS = -D__HDF5_SERIAL',
                            make_inc)

        if '+epw' in spec:
            make('all', 'epw')
        else:
            make('all')

        if 'platform=darwin' in spec:
            mkdirp(prefix.bin)
            for filename in glob.glob("bin/*.x"):
                install(filename, prefix.bin)
        else:
            make('install')
