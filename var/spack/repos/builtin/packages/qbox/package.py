# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Qbox(MakefilePackage):
    """Qbox is a C++/MPI scalable parallel implementation of first-principles
    molecular dynamics (FPMD) based on the plane-wave, pseudopotential
    formalism. Qbox is designed for operation on large parallel computers."""

    homepage = "http://qboxcode.org/"
    url      = "http://qboxcode.org/download/qbox-1.63.7.tgz"

    version('1.63.7', '6b0cf5656f816a1a59e22b268387af33')
    version('1.63.5', 'da3161ab6a455793f2133dd03c04077c')
    version('1.63.4', '8596f32c8fb7e7baa96571c655aaee07')
    version('1.63.2', '55e8f13f37c8e1f43ca831791e3af1da')
    version('1.63.0', '1436c884c553ab026b7f787307e5e6ed')
    version('1.62.3', 'f07e038ab92b85956794e91a40346dbf')
    version('1.60.9', '53b0df612e56bb65e8220d9d9dc8d395')
    version('1.60.4', '060846c9fa03b1f3d7d5ce24a9491de2')
    version('1.60.0', '3856cdc38a27dc17705844c4b9241a21')
    version('1.58.0', 'ec0e6b79fa0ed06742212b1142e36b6a')
    version('1.56.2', 'df7a4217d059a5d351d92e480ed14112')
    version('1.54.4', '8f1a23af7d871317de93810b664ad3aa')
    version('1.54.2', 'aeefee061255dbb36ca7e49378f63ad5')
    version('1.52.3', '1862f2b2056cdf49ec4f746d45a7f1a6')
    version('1.52.2', 'e406deb4c46176f1c15c226868bf61e2')
    version('1.50.4', 'b06ff877257884e4fac321fb5a486266')
    version('1.50.2', '171660b1bb5e57637f019fef055fb764')
    version('1.50.1', '1da528b39da134f86f134432e8fada79')
    version('1.47.0', '86f402651d440e05adc94168d6105da7')
    version('1.45.3', '73b99a73dcbb1b5be9f66f3284750205')
    version('1.45.1', '59e0c2583769b7586981c0d6ffa1b267')
    version('1.45.0', '2c5bfbadfffd330c8c2fe294a10a08e4')
    version('1.44.0', 'c46a2f0f68fe9229aa77779da188cea9')

    variant('mkl', default=False, description="Use MKL for blas, scalapack and fftw")
    variant('openmp', default=False, description="Build with OpenMP support")

    depends_on('mpi')
    depends_on('mkl', when='+mkl') #sjl: how do i get the mkl fftw headers into the flags list?
    depends_on('blas', when='-mkl')
    depends_on('scalapack', when='-mkl')
    depends_on('fftw@3', when='-mkl')
    # depends_on xerces_c@2.8.0 or xerces_c@3 
    depends_on('xerces-c@2.8.0:3')

    build_directory = 'src'

    def edit(self, spec, prefix):
        with open('src/spack.mk', 'w') as mkfile:
            mkfile.write('CXX = {0}\n'.format(spec['mpi'].mpicxx))
            mkfile.write('LD = $(CXX)\n')
            flags = ['-g', '-O3']
            dflags = ['', '_LARGEFILE_SOURCE', 'USE_MPI', 'USE_XERCES',
                      'PARALLEL_FS', 'SCALAPACK', 'ADD_',
                      'USE_FFTW3', 'FFTWMEASURE' ]
            # other dflags that might appear in older versions:
            # _FILE_OFFSET_BITS=64, MPICH_IGNORE_CXX_SEEK, 
            # XML_USE_NO_THREADS, APP_NO_THREADS
            libs = spec['xerces-c'].libs
            ldflags = [''] # for mkl scalapack flags with static linking

            # specifics:
            if '%intel' in spec:
                flags += ['', '-no-prec-div', '-fp-model fast=2', '-ipo']

            if '+openmp' in spec:
                flags += [self.compiler.openmp_flag]
                dflags += ['USE_FFTW3_THREADS']
            else:
                dflags += ['USE_FFTW3_2D']

            if 'xerces-c@3' in spec:
                dflags += ['XERCESC_3']
                
            if '+mkl' in spec:
                # why can't I just check for arch=cray?
                if 'arch=cray-cnl6-haswell' in spec or 'arch=cray-cnl6-ivybridge' in spec:
                    # the "static" here seems inelegant, shouldn't it happen 
                    # automatically (at link time as well as compile time)?
                    flags += ['-static', '-mkl']
                # how to add -I${MKLROOT}/include/fftw ?
                # I suspect it is something like:
                flags += [ '-I{0}/fftw'.format(spec['mkl'].prefix.include) ]
                dflags += ['USE_FFTW3MKL']
                # this might only be for cray, with static linking:
                libdir=spec['mkl'].prefix.lib + '/intel64'
                ldflags += ['-mkl', '-Wl,--start-group', libdir+'/libmkl_scalapack_lp64.a',
                            libdir+'/libmkl_core.a', libdir+'/libmkl_intel_thread.a',
                            libdir+'/libmkl_blacs_intelmpi_lp64.a', '-Wl,--end-group'] 
            else:
                libs += spec['fftw'].libs + spec['scalapack'].libs + spec['blas'].libs

            mkfile.write('# using spec: {0}\n'.format(spec))
            mkfile.write('DFLAGS = {0}\n'.format(' -D'.join(dflags)))
            mkfile.write('CXXFLAGS = {0}\n'.format(' '.join(flags+['$(DFLAGS)'])))
            linkflags=' '.join(['$(CXXFLAGS)']+ldflags)
            mkfile.write('LDFLAGS = {0} {1}\n'.format(libs.ld_flags, linkflags))
        filter_file('$(TARGET)', 'spack', 'src/Makefile', string=True)

    def install(self, spec, prefix):
        mkdir(prefix.src)
        install('src/qb', prefix.src)
        install_tree('test', prefix)
        install_tree('xml', prefix)
        install_tree('util', prefix)
