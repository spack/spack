# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


# TODO: respect the spack-profided compiler flags if any

# TODO: add MKL and BLIS support
# Attention! MKL and BLIS are NOT JUST drop-in replacements
# for blas/lapack!

# TODO: Check that spack-provided  compiler flags 
# are respected

# Attention!
# Dynamic linking *appears* to work fine, but
# Elk is expected to be linked statically. 

# TODO: check if it is possible/reasonable to disable OpenMP
# It doesn't appear to be this way, but check anyway


from spack import *


class Elk(MakefilePackage):
    """Elk code is an advanced dft code aimed at material discovery
    """

    homepage = "https://elk.sourceforge.io/"
    url      = "https://downloads.sourceforge.net/project/elk/elk-7.1.14.tgz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']
    version('7.1.14', sha256='7c2ff30f4b1d72d5dc116de9d70761f2c206700c69d85dd82a17a5a6374453d2')
 

    #parallel builds might fail
    parallel = False
    #mpi support is optional, it is possible to use openmp parallelist only
    variant('mpi', default='False')
    depends_on('mpi', when='+mpi')

    #Elk comes with internal blas and lapack. It also can
    #integrate with openblas and mkl, but requires special code
    #to do so. I've no idea if generic externals like blas-atlas
    #are supported, and besides MKL also interacts with fft capabilities
    #so the only supported options ATM are 'internal' and 'openblas'
    #Consult upstream before changing this.
    #NOTE: weird messages about illegal preprocessing instructions 
    #were observed during compilation of internal linal libs. Didn't test
    variant('linal', default='internal'
            , description='linear algebra libraries to use'
            , values=('internal', 'openblas')
            , multi=False
            )
    depends_on('openblas', when='linal=openblas')
    
    #elk comes with internal FFT lib. It also can use libfftw and MKL FFT
    #currently only internal fft and fftw libs are supported
    #TODO:Add MKL FFT support if possible but see the previous comment.
    variant('fft', default='internal'
            , description='fft library to use;'
            , values=('internal','fftw')
            , multi=False
            )
    depends_on('fftw@3:', when='fft=fftw')

    variant('wannier90', default=False
            , description="support for wannier code. requires wannier library"
            )
    depends_on('wannier90', when="+wannier90")
    
    variant('libxc', default=False
            , description="support for libxc library of functionals for DFT"
            )
    #Note! libxc changed API/ABI around v5, 
    #Linking with older version might not work
    depends_on('libxc@5:', when='+libxc')

   
    #setup is done in make.inc
    #Elk has setup script to generate templates, 
    #you should consult it before changing how we
    #generate make.inc.
    def edit(self, spec, prefix):
        #Defult configuration
        #this appears to be configurable, for whatever reason
        elk_make = 'make'
        #default linear algebra libs
        lib_lpk   = 'lapack.a blas.a' #
        #we do not support linking against mkl yet, activate stub
        src_mkl = 'mkl_stub.f90'
        #we do not support linking against blis yet, activate stub
        src_blis = 'blis_stub.f90'
        #we will overwrite this if we detect request for 
        #openblas support. ATM activate stub
        src_oblas = 'oblas_stub.f90'
        #we will overwrite this if we detect request for 
        #libxc support. ATM activate stub
        src_libxc = 'libxcifc_stub.f90'
        lib_libxc = '  '
        #we will overwrite this if we detect request for 
        #fftw support. ATM activate stub
        src_fft = 'zfftifc.f90'
        lib_fft = 'fftlib.a' 
        #we will overwrite this if we detect request for 
        #wannier90 support. ATM activate stub
        src_w90s = 'w90_stub.f90'
        lib_w90  = '  '
        #default compiler flags used in elk
        dfflags  = "-O3 -ffast-math -funroll-loops -fopenmp"
        #elkFC = mpiCC/FC fi +mpi of CC/FC otherwise
        #elk uses a stub module in case MPI is absent.
        if '+mpi' in spec :
            elk_f77     = spec['mpi'].mpif77
            elk_f90     = spec['mpi'].mpifc
            src_mpi     = ' '
        else :
            elk_f77     = spack_f77
            elk_f90     = spack_fc
            src_mpi     = 'mpi_stub.f90'
        #elk blas+lapack
        #elk requires specific stubs for missing openblas and mkl
        #we do not support linking against mkl yet.
        if 'linal=openblas' in spec :
            lib_lpk   = '-lopenblas'
            src_oblas = '  '
        if  'fft=fftw' in spec :
            lib_fft = '-lfftw3'
            src_fft = 'zfftifc_fftw.f90'
        if '+libxc' in spec :
            src_libxc = 'libxcf90.f90 libxcifc.f90'
            lib_libxc = '-lxcf90 -lxc'
        if '+wannier90' in spec :
            src_w90s = '  '
            lib_w90  = '-lwannier'
        #write generated config into make.inc
        with open('make.inc', 'w') as inc :
            inc.write('{0} = {1} \n'.format('MAKE',      'make' ))
            inc.write('{0} = {1} \n'.format('F77',       elk_f77))
            inc.write('{0} = {1} \n'.format('F90',       elk_f90 ))
            inc.write('{0} = {1} \n'.format('F77_OPTS',  dfflags ))
            inc.write('{0} = {1} \n'.format('F90_OPTS',  dfflags ))
            inc.write('{0} = {1} \n'.format('LIB_LPK',   lib_lpk ))
            inc.write('{0} = {1} \n'.format('LIB_FFT',   lib_fft ))
            inc.write('{0} = {1} \n'.format('SRC_FFT',   src_fft ))
            inc.write('{0} = {1} \n'.format('SRC_MPI',   src_mpi ))
            inc.write('{0} = {1} \n'.format('SRC_MKL',   src_mkl))
            inc.write('{0} = {1} \n'.format('SRC_OBLAS', src_oblas ))
            inc.write('{0} = {1} \n'.format('SRC_BLIS',  src_blis ))
            inc.write('{0} = {1} \n'.format('LIB_libxc', lib_libxc ))
            inc.write('{0} = {1} \n'.format('SRC_libxc', src_libxc ))
            inc.write('{0} = {1} \n'.format('SRC_W90S',  src_w90s ))
            inc.write('{0} = {1} \n'.format('LIB_W90',   lib_w90))
#            inc.write('{0} = {1} \n'.format('', ))
        #end with open
    #end def edit

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('src/elk',                   prefix.bin)
        install('src/eos/eos',               prefix.bin)
        install('src/spacegroup/spacegroup', prefix.bin)
        install_tree('examples', join_path(prefix, 'examples'))
        install_tree('species',  join_path(prefix, 'species'))

