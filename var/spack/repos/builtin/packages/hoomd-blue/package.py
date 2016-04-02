from spack import *
import os

class HoomdBlue(Package):
    """HOOMD-blue is a general-purpose particle simulation toolkit. It scales
    from a single CPU core to thousands of GPUs.

    You define particle initial conditions and interactions in a high-level
    python script. Then tell HOOMD-blue how you want to execute the job and it
    takes care of the rest. Python job scripts give you unlimited flexibility
    to create custom initialization routines, control simulation parameters,
    and perform in situ analysis."""

    homepage = "https://codeblue.umich.edu/hoomd-blue/index.html"
    url      = "https://bitbucket.org/glotzer/hoomd-blue/get/v1.3.3.tar.bz2"

    version('1.3.3', '1469ef4531dc14b579c0acddbfe6a273')

    variant('mpi',  default=True, description='Compile with MPI enabled')
    variant('cuda', default=True, description='Compile with CUDA Toolkit')
    variant('doc',  default=True, description='Generate documentation')

    extends('python')
    depends_on('py-numpy')
    depends_on('boost+python')
    depends_on('cmake')
    depends_on('mpi', when='+mpi')
    depends_on('cuda', when='+cuda')
    depends_on('doxygen', when='+doc')

    def install(self, spec, prefix):

        cmake_args = [
            '-DPYTHON_EXECUTABLE=%s/python' % spec['python'].prefix.bin,
            '-DBOOST_ROOT=%s'               % spec['boost' ].prefix
        ]

        # MPI support
        if '+mpi' in spec:
            os.environ['MPI_HOME'] = spec['mpi'].prefix
            cmake_args.append('-DENABLE_MPI=ON')
        else:
            cmake_args.append('-DENABLE_MPI=OFF')

        # CUDA support
        if '+cuda' in spec:
            cmake_args.append('-DENABLE_CUDA=ON')
        else:
            cmake_args.append('-DENABLE_CUDA=OFF')

        # CUDA-aware MPI library support
        #if '+cuda' in spec and '+mpi' in spec:
        #    cmake_args.append('-DENABLE_MPI_CUDA=ON')
        #else:
        #    cmake_args.append('-DENABLE_MPI_CUDA=OFF')

        # There may be a bug in the MPI-CUDA code. See:
        # https://groups.google.com/forum/#!msg/hoomd-users/2griTESmc5I/E69s_M5fDwAJ
        # This prevented "make test" from passing for me.
        cmake_args.append('-DENABLE_MPI_CUDA=OFF')

        # Documentation
        if '+doc' in spec:
            cmake_args.append('-DENABLE_DOXYGEN=ON')
        else:
            cmake_args.append('-DENABLE_DOXYGEN=OFF')

        cmake_args.extend(std_cmake_args)
        cmake('.', *cmake_args)

        make()
        make("test")
        make("install")
