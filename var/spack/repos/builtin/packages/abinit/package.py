# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class Abinit(AutotoolsPackage):
    """ABINIT is a package whose main program allows one to find the total
    energy, charge density and electronic structure of systems made of
    electrons and nuclei (molecules and periodic solids) within
    Density Functional Theory (DFT), using pseudopotentials and a planewave
    or wavelet basis.

    ABINIT also includes options to optimize the geometry according to the
    DFT forces and stresses, or to perform molecular dynamics
    simulations using these forces, or to generate dynamical matrices,
    Born effective charges, and dielectric tensors, based on Density-Functional
    Perturbation Theory, and many more properties. Excited states can be
    computed within the Many-Body Perturbation Theory (the GW approximation and
    the Bethe-Salpeter equation), and Time-Dependent Density Functional Theory
    (for molecules). In addition to the main ABINIT code, different utility
    programs are provided.
    """

    homepage = 'https://www.abinit.org/'
    url      = 'https://www.abinit.org/sites/default/files/packages/abinit-8.6.3.tar.gz'

    version('9.6.1', sha256='b6a12760fd728eb4aacca431ae12150609565bedbaa89763f219fcd869f79ac6')
    version('9.4.2', sha256='d40886f5c8b138bb4aa1ca05da23388eb70a682790cfe5020ecce4db1b1a76bc')
    version('8.10.3', sha256='ed626424b4472b93256622fbb9c7645fa3ffb693d4b444b07d488771ea7eaa75')
    version('8.10.2', sha256='4ee2e0329497bf16a9b2719fe0536cc50c5d5a07c65e18edaf15ba02251cbb73')
    version('8.8.2', sha256='15216703bd56a799a249a112b336d07d733627d3756487a4b1cb48ebb625c3e7')
    version('8.6.3', sha256='82e8d071088ab8dc1b3a24380e30b68c544685678314df1213180b449c84ca65')
    version('8.2.2', sha256='e43544a178d758b0deff3011c51ef7c957d7f2df2ce8543366d68016af9f3ea1')
    # Versions before 8.0.8b are not supported.
    version('8.0.8b', sha256='37ad5f0f215d2a36e596383cb6e54de3313842a0390ce8d6b48a423d3ee25af2')

    variant('mpi', default=True,
            description='Builds with MPI support. Requires MPI2+')
    variant('openmp', default=False,
            description='Enables OpenMP threads. Use threaded FFTW3')
    variant('scalapack', default=False,
            description='Enables scalapack support. Requires MPI')

    variant('wannier90', default=False,
            description='Enables the Wannier90 library')
    variant('libxml2', default=False,
            description='Enable libxml2 support, used by multibinit')

    variant('optimization-flavor', default='standard', multi=False,
            values=('safe', 'standard', 'aggressive'),
            description='Select the optimization flavor to use.')

    variant('install-tests', default=False,
            description='Install test cases')

    # Add dependencies
    depends_on('atompaw')
    depends_on('blas')
    depends_on('lapack')

    # Require MPI2+
    depends_on('mpi@2:', when='+mpi')

    depends_on('scalapack', when='+scalapack+mpi')

    depends_on('fftw-api')

    depends_on('netcdf-fortran')
    depends_on('netcdf-c+mpi', when='+mpi')
    depends_on('netcdf-c~mpi', when='~mpi')
    depends_on('hdf5+mpi', when='+mpi')
    depends_on('hdf5~mpi', when='~mpi')
    depends_on("wannier90+shared", when='+wannier90+mpi')

    # constrain libxc version
    depends_on('libxc')
    depends_on('libxc@:2', when='@:8')

    # libxml2
    depends_on('libxml2', when='@9:+libxml2')

    # Cannot ask for +scalapack if it does not depend on MPI
    conflicts('+scalapack', when='~mpi')

    # Cannot ask for +wannier90 if it does not depend on MPI
    conflicts('+wannier90', when='~mpi')

    # libxml2 needs version 9 and above
    conflicts('+libxml2', when='@:8')

    conflicts('%gcc@7:', when='@:8.8')
    conflicts('%gcc@9:', when='@:8.10')

    # need openmp threading for abinit+openmp
    # TODO: The logic here can be reversed with the new concretizer. Instead of
    # using `conflicts`, `depends_on` could be used instead.
    for fftw in ['amdfftw', 'cray-fftw', 'fujitsu-fftw', 'fftw']:
        conflicts('+openmp', when='^{0}~openmp'.format(fftw),
                  msg='Need to request {0} +openmp'.format(fftw))

    mkl_message = 'Need to set dependent variant to threads=openmp'
    conflicts('+openmp',
              when='^intel-mkl threads=none',
              msg=mkl_message)
    conflicts('+openmp',
              when='^intel-mkl threads=tbb',
              msg=mkl_message)
    conflicts('+openmp',
              when='^intel-parallel-studio +mkl threads=none',
              msg=mkl_message)

    conflicts('+openmp',
              when='^fujitsu-ssl2 ~parallel',
              msg='Need to request fujitsu-ssl2 +parallel')

    conflicts('~openmp',
              when='^fujitsu-ssl2 +parallel',
              msg='Need to request fujitsu-ssl2 ~parallel')

    patch('rm_march_settings.patch', when='@:8')
    patch('rm_march_settings_v9.patch', when='@9:')

    # Fix detection of Fujitsu compiler
    # Fix configure not to collect the option that causes an error
    # Fix intent(out) and unnecessary rewind to avoid compile error
    patch('fix_for_fujitsu.patch', when='@:8 %fj')
    patch('fix_for_fujitsu.v9.patch', when='@9: %fj')

    def configure_args(self):

        spec = self.spec

        options = []
        options += self.with_or_without('libxml2')

        oapp = options.append
        if '@:8' in spec:
            oapp('--enable-optim={0}'
                 .format(self.spec.variants['optimization-flavor'].value))
        else:
            oapp('--with-optim-flavor={0}'
                 .format(self.spec.variants['optimization-flavor'].value))

        if '+wannier90' in spec:
            if '@:8' in spec:
                oapp('--with-wannier90-libs=-L{0}'
                     .format(spec['wannier90'].prefix.lib + ' -lwannier -lm'))
                oapp('--with-wannier90-incs=-I{0}'
                     .format(spec['wannier90'].prefix.modules))
                oapp('--with-wannier90-bins={0}'
                     .format(spec['wannier90'].prefix.bin))
                oapp('--enable-connectors')
                oapp('--with-dft-flavor=atompaw+libxc+wannier90')
            else:
                options.extend([
                    'WANNIER90_CPPFLAGS=-I{0}'.format(
                        spec['wannier90'].prefix.modules),
                    'WANNIER90_LIBS=-L{0} {1}'.format(
                        spec['wannier90'].prefix.lib, '-lwannier'),
                ])
        else:
            if '@:8' in spec:
                oapp('--with-dft-flavor=atompaw+libxc')
            else:
                '--without-wannier90',

        if '+mpi' in spec:
            oapp('CC={0}'.format(spec['mpi'].mpicc))
            oapp('CXX={0}'.format(spec['mpi'].mpicxx))
            oapp('FC={0}'.format(spec['mpi'].mpifc))

            # MPI version:
            # let the configure script auto-detect MPI support from mpi_prefix
            if '@:8' in spec:
                oapp('--enable-mpi=yes')
            else:
                oapp('--with-mpi')
        else:
            if '@:8' in spec:
                oapp('--enable-mpi=no')
            else:
                oapp('--without-mpi')

        # Activate OpenMP in Abinit Fortran code.
        if '+openmp' in spec:
            oapp('--enable-openmp=yes')
        else:
            oapp('--enable-openmp=no')

        # BLAS/LAPACK/SCALAPACK-ELPA
        linalg = spec['lapack'].libs + spec['blas'].libs
        if '^mkl' in spec:
            linalg_flavor = 'mkl'
        elif '@9:' in spec and '^openblas' in spec:
            linalg_flavor = 'openblas'
        elif '@9:' in spec and '^fujitsu-ssl2' in spec:
            linalg_flavor = 'openblas'
        else:
            linalg_flavor = 'custom'

        if '+scalapack' in spec:
            linalg = spec['scalapack'].libs + linalg
            if '@:8' in spec:
                linalg_flavor = 'scalapack+{0}'.format(linalg_flavor)

        if '@:8' in spec:
            oapp('--with-linalg-libs={0}'.format(linalg.ld_flags))
        else:
            oapp('LINALG_LIBS={0}'.format(linalg.ld_flags))

        oapp('--with-linalg-flavor={0}'.format(linalg_flavor))

        if '^mkl' in spec:
            fftflavor = 'dfti'
        else:
            if '+openmp' in spec:
                fftflavor, fftlibs = 'fftw3-threads', '-lfftw3_omp -lfftw3 -lfftw3f'
            else:
                fftflavor, fftlibs = 'fftw3', '-lfftw3 -lfftw3f'

        oapp('--with-fft-flavor={0}'.format(fftflavor))

        if '@:8' in spec:
            if '^mkl' in spec:
                oapp('--with-fft-incs={0}'.format(spec['fftw-api'].headers.cpp_flags))
                oapp('--with-fft-libs={0}'.format(spec['fftw-api'].libs.ld_flags))
            else:
                options.extend([
                    '--with-fft-incs={0}'.format(spec['fftw-api'].headers.cpp_flags),
                    '--with-fft-libs=-L{0} {1}'.format(
                        spec['fftw-api'].prefix.lib, fftlibs),
                ])
        else:
            if '^mkl' in spec:
                options.extend([
                    'FFT_CPPFLAGS={0}'.format(spec['fftw-api'].headers.cpp_flags),
                    'FFT_LIBs={0}'.format(spec['fftw-api'].libs.ld_flags),
                ])
            else:
                options.extend([
                    'FFTW3_CPPFLAGS={0}'.format(spec['fftw-api'].headers.cpp_flags),
                    'FFTW3_LIBS=-L{0} {1}'.format(
                        spec['fftw-api'].prefix.lib, fftlibs),
                ])

        # LibXC library
        libxc = spec['libxc:fortran']
        if '@:8' in spec:
            options.extend([
                '--with-libxc-incs={0}'.format(libxc.headers.cpp_flags),
                '--with-libxc-libs={0}'.format(libxc.libs.ld_flags + ' -lm')
            ])
        else:
            oapp('--with-libxc={0}'.format(libxc.prefix))

        # Netcdf4/HDF5
        hdf5 = spec['hdf5:hl']
        netcdfc = spec['netcdf-c']
        netcdff = spec['netcdf-fortran:shared']
        if '@:8' in spec:
            oapp('--with-trio-flavor=netcdf')
            # Since version 8, Abinit started to use netcdf4 + hdf5 and we have
            # to link with the high level HDF5 library
            options.extend([
                '--with-netcdf-incs={0}'.format(
                    netcdfc.headers.cpp_flags + ' ' +
                    netcdff.headers.cpp_flags),
                '--with-netcdf-libs={0}'.format(
                    netcdff.libs.ld_flags + ' ' + hdf5.libs.ld_flags
                ),
            ])
        else:
            options.extend([
                '--with-netcdf={0}'.format(netcdfc.prefix),
                '--with-netcdf-fortran={0}'.format(netcdff.prefix),
            ])

        if self.spec.satisfies('%fj'):
            oapp('FCFLAGS_MODDIR=-M{0}'.format(join_path(
                 self.stage.source_path, 'src/mods')))

        return options

    def check(self):
        """This method is called after the build phase if tests have been
        explicitly activated by user.
        """
        make('check')

        # the tests directly execute abinit. thus failing with MPI
        # TODO: run tests in tests/ via the builtin runtests.py
        #       requires Python with numpy, pyyaml, pandas
        if '~mpi' in self.spec:
            make('tests_in')

    def install(self, spec, prefix):
        make('install')
        if '+install-tests' in spec:
            install_tree('tests', spec.prefix.tests)
