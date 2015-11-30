from spack import *

class OmptOpenmp(Package):
    """LLVM/Clang OpenMP runtime with OMPT support. This is a fork of the OpenMPToolsInterface/LLVM-openmp fork of the official LLVM OpenMP mirror.  This library provides a drop-in replacement of the OpenMP runtimes for GCC, Intel and LLVM/Clang."""
    homepage = "https://github.com/OpenMPToolsInterface/LLVM-openmp"
    url      = "http://github.com/khuck/LLVM-openmp/archive/v0.1.tar.gz"

    version('0.1', '2334e6a84b52da41b27afd9831ed5370')

    # depends_on("foo")

    def install(self, spec, prefix):
        with working_dir("runtime/build", create=True):

            # FIXME: Modify the configure line to suit your build system here.
            cmake('-DCMAKE_C_COMPILER=%s' % self.compiler.cc, 
                  '-DCMAKE_CXX_COMPILER=%s' % self.compiler.cxx,
                  '-DCMAKE_INSTALL_PREFIX=%s' % prefix,
                  '..', *std_cmake_args)

            # FIXME: Add logic to build and install here
            make()
            make("install")
