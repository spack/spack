from spack import *
import socket
import os
from os.path import join as pjoin

class Fastmath(Package):
    """Wrapper package to install all FASTMath packages."""

    homepage = "www.fastmath-scidac.org/"

    version('1.0', 'bf5b7a996baebe97d6bf1801604a7e7b')

    depends_on('blas')
    depends_on('lapack')
    depends_on('parmetis')
    depends_on('metis')
    depends_on('sundials')
    depends_on('cblas')
    depends_on('hypre')
    depends_on('hdf5')
    depends_on('netcdf')
    depends_on('superlu')
    depends_on('zoltan_distrib')
    depends_on('cgm')
    depends_on('moab')
    depends_on('petsc')
    depends_on('arpack')
    depends_on('parpack')
    depends_on('boxlib')

    def url_for_version(self, version):
        print __file__
        dummy_tar_path =  os.path.abspath(pjoin(os.path.split(__file__)[0]))
        dummy_tar_path = pjoin(dummy_tar_path,"fastmath.tar.gz")
        url      = "file://" + dummy_tar_path
        return url

    def install(self, spec, prefix):
        dest_dir     = env["SPACK_DEBUG_LOG_DIR"]
        c_compiler   = env["SPACK_CC"]
        cpp_compiler = env["SPACK_CXX"]
        sys_type     = spec.architecture
        if env.has_key("SYS_TYPE"):
            sys_type = env["SYS_TYPE"]
        # TODO: better name (use sys-type and compiler name ?)
        print "cmake executable: %s" % cmake_exe
        cfg = open(pjoin(dest_dir,"%s.cmake" % socket.gethostname()),"w")
        cfg.close()        
