# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import copy

from spack import *


class Cp2k(Package):
    """CP2K is a quantum chemistry and solid state physics software package
    that can perform atomistic simulations of solid state, liquid, molecular,
    periodic, material, crystal, and biological systems
    """
    homepage = 'https://www.cp2k.org'
    url = 'https://github.com/cp2k/cp2k/releases/download/v3.0.0/cp2k-3.0.tar.bz2'
    list_url = 'https://github.com/cp2k/cp2k/releases'

    version('6.1', '573a4de5a0ee2aaabb213e04543cb10f')
    version('5.1', 'f25cf301aec471d7059179de4dac3ee7')
    version('4.1', 'b0534b530592de15ac89828b1541185e')
    version('3.0', 'c05bc47335f68597a310b1ed75601d35')

    variant('mpi', default=True, description='Enable MPI support')
    variant('blas', default='openblas', values=('openblas', 'mkl', 'accelerate'),
            description='Enable the use of OpenBlas/MKL/Accelerate')
    variant('openmp', default=False, description='Enable OpenMP support')
    variant('smm', default='libxsmm', values=('libxsmm', 'libsmm', 'blas'),
            description='Library for small matrix multiplications')
    variant('plumed', default=False, description='Enable PLUMED support')
    variant('libxc', default=True,
            description='Support additional functionals via libxc')
    variant('pexsi', default=False,
            description=('Enable the alternative PEXSI method'
                         'for density matrix evaluation'))
    variant('elpa', default=False,
            description='Enable optimised diagonalisation routines from ELPA')

    depends_on('python', type='build')

    depends_on('fftw@3:', when='~openmp')
    depends_on('fftw@3:+openmp', when='+openmp')

    # see #1712 for the reason to enumerate BLAS libraries here
    depends_on('openblas threads=none', when='blas=openblas ~openmp')
    depends_on('openblas threads=openmp', when='blas=openblas +openmp')
    depends_on('lapack', when='blas=openblas ~openmp')

    depends_on('intel-mkl', when="blas=mkl ~openmp")
    depends_on('intel-mkl threads=openmp', when='blas=mkl +openmp')

    conflicts('blas=accelerate', '+openmp')  # there is no Accelerate with OpenMP support

    depends_on('libxsmm@1.10:~header-only', when='smm=libxsmm')
    # use pkg-config (support added in libxsmm-1.10) to link to libxsmm
    depends_on('pkgconfig', type='build', when='smm=libxsmm')

    # libint & libxc are always statically linked
    depends_on('libint@1.1.4:1.2', when='@3.0:6.999', type='build')
    depends_on('libxc@2.2.2:', when='+libxc@:5.5999', type='build')
    depends_on('libxc@4.0.3:', when='+libxc@6.0:', type='build')

    depends_on('mpi@2:', when='+mpi')
    depends_on('scalapack', when='+mpi')
    depends_on('elpa@2011.12:2016.13+openmp', when='+openmp+elpa@:5.999')
    depends_on('elpa@2011.12:2017.11+openmp', when='+openmp+elpa@6.0:')
    depends_on('elpa@2011.12:2016.13~openmp', when='~openmp+elpa@:5.999')
    depends_on('elpa@2011.12:2017.11~openmp', when='~openmp+elpa@6.0:')
    depends_on('plumed+shared+mpi', when='+plumed+mpi')
    depends_on('plumed+shared~mpi', when='+plumed~mpi')

    # while we link statically against PEXSI, its own deps may be linked in
    # dynamically, therefore can't set this as pure build-type dependency.
    depends_on('pexsi+fortran@0.9.0:0.9.999', when='+pexsi@:4.999')
    depends_on('pexsi+fortran@0.10.0:', when='+pexsi@5.0:')

    # PEXSI and ELPA need MPI in CP2K
    conflicts('~mpi', '+pexsi')
    conflicts('~mpi', '+elpa')

    # Apparently cp2k@4.1 needs an "experimental" version of libwannier.a
    # which is only available contacting the developer directly. See INSTALL
    # in the stage of cp2k@4.1
    depends_on('wannier90', when='@3.0+mpi', type='build')

    # TODO : add dependency on CUDA

    # CP2K needs compiler specific compilation flags, e.g. optflags
    conflicts('%clang')
    conflicts('%cray')
    conflicts('%nag')
    conflicts('%xl')

    def install(self, spec, prefix):
        # Construct a proper filename for the architecture file
        cp2k_architecture = '{0.architecture}-{0.compiler.name}'.format(spec)
        cp2k_version = ('{prefix}{suffix}'
                        .format(prefix='p' if '+mpi' in spec else 's',
                                suffix='smp' if '+openmp' in spec else 'opt'))

        makefile_basename = '.'.join([cp2k_architecture, cp2k_version])
        makefile = join_path('arch', makefile_basename)

        # Write the custom makefile
        with open(makefile, 'w') as mkf:
            # Optimization flags
            optflags = {
                'gcc': [
                    '-O2',
                    '-mtune=native',
                    '-funroll-loops',
                    '-ffast-math',
                    '-ftree-vectorize',
                ],
                'intel': [
                    '-O2',
                    '-pc64',
                    '-unroll',
                ],
                'pgi': [
                    '-fast',
                ],
            }

            dflags = ['-DNDEBUG']

            if '+openmp' in spec:
                fftw = spec['fftw:openmp']
            else:
                fftw = spec['fftw']

            cppflags = [
                '-D__FFTW3',
                '-D__LIBINT',
                '-D__LIBINT_MAX_AM=6',
                '-D__LIBDERIV_MAX_AM1=5',
                fftw.headers.cpp_flags,
            ]

            if '^mpi@3:' in spec:
                cppflags.append('-D__MPI_VERSION=3')
            elif '^mpi@2:' in spec:
                cppflags.append('-D__MPI_VERSION=2')

            if '^intel-mkl' in spec:
                cppflags.append('-D__FFTSG')

            cflags = copy.deepcopy(optflags[self.spec.compiler.name])
            cxxflags = copy.deepcopy(optflags[self.spec.compiler.name])
            fcflags = copy.deepcopy(optflags[self.spec.compiler.name])
            ldflags = []
            libs = []

            if '%intel' in spec:
                cflags.append('-fp-model precise')
                cxxflags.append('-fp-model precise')
                fcflags.extend(['-fp-model source', '-heap-arrays 64'])
                if '+openmp' in spec:
                    fcflags.append('-openmp')
                    ldflags.append('-openmp')
            elif '%gcc' in spec:
                fcflags.extend(['-ffree-form', '-ffree-line-length-none'])
                if '+openmp' in spec:
                    fcflags.append('-fopenmp')
                    ldflags.append('-fopenmp')
            elif '%pgi' in spec:
                fcflags.extend(['-Mfreeform', '-Mextend'])
                if '+openmp' in spec:
                    fcflags.append('-mp')
                    ldflags.append('-mp')

            ldflags.append(fftw.libs.search_flags)

            if 'superlu-dist@4.3' in spec:
                ldflags.insert(0, '-Wl,--allow-multiple-definition')

            # libint-1.x.y has to be linked statically to work around
            # inconsistencies in its Fortran interface definition
            # (short-int vs int) which otherwise causes segfaults at runtime
            # due to wrong offsets into the shared library symbols.
            libs.extend([
                join_path(spec['libint'].libs.directories[0], 'libderiv.a'),
                join_path(spec['libint'].libs.directories[0], 'libint.a'),
            ])

            if '+plumed' in self.spec:
                # Include Plumed.inc in the Makefile
                mkf.write('include {0}\n'.format(
                    join_path(self.spec['plumed'].prefix.lib,
                              'plumed',
                              'src',
                              'lib',
                              'Plumed.inc')
                ))
                # Add required macro
                dflags.extend(['-D__PLUMED2'])
                cppflags.extend(['-D__PLUMED2'])
                libs.extend([
                    join_path(self.spec['plumed'].prefix.lib,
                              'libplumed.{0}'.format(dso_suffix))
                ])

            mkf.write('CC = {0.compiler.cc}\n'.format(self))
            if '%intel' in self.spec:
                # CPP is a commented command in Intel arch of CP2K
                # This is the hack through which cp2k developers avoid doing :
                #
                # ${CPP} <file>.F > <file>.f90
                #
                # and use `-fpp` instead
                mkf.write('CPP = # {0.compiler.cc} -P\n\n'.format(self))
                mkf.write('AR = xiar -r\n\n')
            else:
                mkf.write('CPP = # {0.compiler.cc} -E\n\n'.format(self))
                mkf.write('AR = ar -r\n\n')
            fc = self.compiler.fc if '~mpi' in spec else self.spec['mpi'].mpifc
            mkf.write('FC = {0}\n'.format(fc))
            mkf.write('LD = {0}\n'.format(fc))

            # Intel
            if '%intel' in self.spec:
                cppflags.extend([
                    '-D__INTEL',
                    '-D__HAS_ISO_C_BINDING',
                    '-D__USE_CP2K_TRACE',
                    '-D__MKL'
                ])
                fcflags.extend([
                    '-diag-disable 8290,8291,10010,10212,11060',
                    '-free',
                    '-fpp'
                ])

            # FFTW, LAPACK, BLAS
            lapack = spec['lapack'].libs
            blas = spec['blas'].libs
            ldflags.append((lapack + blas).search_flags)
            libs.extend([str(x) for x in (fftw.libs, lapack, blas)])

            # MPI
            if '+mpi' in self.spec:
                cppflags.extend([
                    '-D__parallel',
                    '-D__SCALAPACK'
                ])

                scalapack = spec['scalapack'].libs
                ldflags.append(scalapack.search_flags)

                libs.extend(scalapack)
                libs.extend(self.spec['mpi:cxx'].libs)
                libs.extend(self.compiler.stdcxx_libs)

                if 'wannier90' in spec:
                    cppflags.append('-D__WANNIER90')
                    wannier = join_path(
                        spec['wannier90'].libs.directories[0], 'libwannier.a'
                    )
                    libs.append(wannier)

            if '+libxc' in spec:
                libxc = spec['libxc:fortran,static']
                cppflags += [
                    '-D__LIBXC',
                    libxc.headers.cpp_flags
                ]

                ldflags.append(libxc.libs.search_flags)
                libs.append(str(libxc.libs))

            if '+pexsi' in self.spec:
                cppflags.append('-D__LIBPEXSI')
                fcflags.append('-I' + join_path(
                    spec['pexsi'].prefix, 'fortran'))
                libs.extend([
                    join_path(spec['pexsi'].libs.directories[0],
                              'libpexsi.a'),
                    join_path(spec['superlu-dist'].libs.directories[0],
                              'libsuperlu_dist.a'),
                    join_path(
                        spec['parmetis'].libs.directories[0],
                        'libparmetis.{0}'.format(dso_suffix)
                    ),
                    join_path(
                        spec['metis'].libs.directories[0],
                        'libmetis.{0}'.format(dso_suffix)
                    ),
                ])

            if '+elpa' in self.spec:
                elpa = spec['elpa']
                elpa_suffix = '_openmp' if '+openmp' in elpa else ''
                elpa_base_path = join_path(
                    elpa.prefix,
                    'include',
                    'elpa{suffix}-{version!s}'.format(
                        suffix=elpa_suffix, version=elpa.version))

                fcflags.append('-I' + join_path(elpa_base_path, 'modules'))
                libs.append(join_path(elpa.libs.directories[0],
                                      ('libelpa{elpa_suffix}.{dso_suffix}'
                                       .format(elpa_suffix=elpa_suffix,
                                               dso_suffix=dso_suffix))))

                if spec.satisfies('@:4.999'):
                    if elpa.satisfies('@:2014.5.999'):
                        cppflags.append('-D__ELPA')
                    elif elpa.satisfies('@2014.6:2015.10.999'):
                        cppflags.append('-D__ELPA2')
                    else:
                        cppflags.append('-D__ELPA3')
                else:
                    cppflags.append('-D__ELPA={0}{1:02d}'
                                    .format(elpa.version[0],
                                            int(elpa.version[1])))
                    fcflags.append('-I' + join_path(elpa_base_path, 'elpa'))

            if 'smm=libsmm' in spec:
                lib_dir = join_path('lib', cp2k_architecture, cp2k_version)
                mkdirp(lib_dir)
                try:
                    copy(env['LIBSMM_PATH'], join_path(lib_dir, 'libsmm.a'))
                except KeyError:
                    raise KeyError('Point environment variable LIBSMM_PATH to '
                                   'the absolute path of the libsmm.a file')
                except IOError:
                    raise IOError('The file LIBSMM_PATH pointed to does not '
                                  'exist. Note that it must be absolute path.')
                cppflags.extend([
                    '-D__HAS_smm_dnn',
                    '-D__HAS_smm_vec',
                ])
                libs.append('-lsmm')
            elif 'smm=libxsmm' in spec:
                cppflags.extend([
                    '-D__LIBXSMM',
                    '$(shell pkg-config --cflags-only-other libxsmmf)',
                ])
                fcflags.append('$(shell pkg-config --cflags-only-I libxsmmf)')
                libs.append('$(shell pkg-config --libs libxsmmf)')

            dflags.extend(cppflags)
            cflags.extend(cppflags)
            cxxflags.extend(cppflags)
            fcflags.extend(cppflags)

            # Write compiler flags to file
            mkf.write('DFLAGS = {0}\n\n'.format(' '.join(dflags)))
            mkf.write('CPPFLAGS = {0}\n\n'.format(' '.join(cppflags)))
            mkf.write('CFLAGS = {0}\n\n'.format(' '.join(cflags)))
            mkf.write('CXXFLAGS = {0}\n\n'.format(' '.join(cxxflags)))
            mkf.write('FCFLAGS = {0}\n\n'.format(' '.join(fcflags)))
            mkf.write('LDFLAGS = {0}\n\n'.format(' '.join(ldflags)))
            if '%intel' in spec:
                mkf.write('LDFLAGS_C = {0}\n\n'.format(
                    ' '.join(ldflags) + ' -nofor_main')
                )
            mkf.write('LIBS = {0}\n\n'.format(' '.join(libs)))
            mkf.write('DATA_DIR = {0}\n\n'.format(self.prefix.share.data))

        with working_dir('makefiles'):
            # Apparently the Makefile bases its paths on PWD
            # so we need to set PWD = os.getcwd()
            pwd_backup = env['PWD']
            env['PWD'] = os.getcwd()
            make('ARCH={0}'.format(cp2k_architecture),
                 'VERSION={0}'.format(cp2k_version))
            env['PWD'] = pwd_backup
        exe_dir = join_path('exe', cp2k_architecture)
        install_tree(exe_dir, self.prefix.bin)
        install_tree('data', self.prefix.share.data)
