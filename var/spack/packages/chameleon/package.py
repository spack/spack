from spack import *
import os

class Chameleon(Package):
    """Dense Linear Algebra for Scalable Multi-core Architectures and GPGPUs"""
    homepage = "https://project.inria.fr/chameleon/"
    url      = "http://morse.gforge.inria.fr/chameleon-0.9.1.tar.gz"

    # Install from sources
    if os.environ.has_key("MORSE_CHAMELEON_TAR") and os.environ.has_key("MORSE_CHAMELEON_TAR_MD5"):
        version('local', '%s' % os.environ['MORSE_CHAMELEON_TAR_MD5'],
                url = "file://%s" % os.environ['MORSE_CHAMELEON_TAR'])
    else:
        version('0.9.0', '67679f3376d4ac4575cc8433a3329abb')
        version('0.9.1', 'fa21b7c44daf34e540ed837a9263772d')

    #variant('debug', default=False, description='Enable debug symbols')
    variant('mpi', default=False, description='Enable MPI')
    variant('cuda', default=False, description='Enable CUDA')
    variant('magma', default=False, description='Enable MAGMA kernels')
    variant('fxt', default=False, description='Enable FxT tracing support through StarPU')
    variant('simu', default=False, description='Enable simulation mode through StarPU+SimGrid')

    #depends_on("cblas")
    #depends_on("lapacke")
    depends_on("starpu")
    depends_on("mpi", when='+mpi')
    depends_on("magma", when='+magma')
    depends_on("fxt", when='+fxt')

    def install(self, spec, prefix):

        with working_dir('spack-build', create=True):

            cmake_args = [
                "..",
                "-DBUILD_SHARED_LIBS=ON"]

            #if '+debug' in spec:
                # Enable Debug here.
            #cmake_args.extend(["-DCMAKE_BUILD_TYPE=Debug"])

            if '+mpi' in spec:
                # Enable MPI here.
                cmake_args.extend(["-DCHAMELEON_USE_MPI=ON"])
            if '+cuda' in spec:
                # Enable CUDA here.
                cmake_args.extend(["-DCHAMELEON_USE_CUDA=ON"])
            if '+magma' in spec:
                # Enable MAGMA here.
                cmake_args.extend(["-DCHAMELEON_USE_MAGMA=ON"])
            if '+fxt' in spec:
                # Enable FxT here.
                cmake_args.extend(["-DCHAMELEON_USE_FXT=ON"])
            if '+simu' in spec:
                # Enable SimGrid here.
                cmake_args.extend(["-DCHAMELEON_SIMULATION=ON"])

            cmake_args.extend(std_cmake_args)

            #print cmake_args

            cmake(*cmake_args)
            make()
            make("install")
