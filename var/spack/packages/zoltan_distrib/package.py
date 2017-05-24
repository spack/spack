from spack import *

class ZoltanDistrib(Package):
    """The Zoltan Library provides critical data-management services to a wide range of parallel applications."""
    homepage = "http://www.cs.sandia.gov/Zoltan/"
    url      = "http://www.cs.sandia.gov/~kddevin/Zoltan_Distributions/zoltan_distrib_v3.82.tar.gz"

    version('3.82', '2bcc852bedee873f3d21b519611605d0')

    depends_on("parmetis")

    def install(self, spec, prefix):
        # mkdir("./BUILD_DIR")
        # cd("./BUILD_DIR")
        
        with working_dir('BUILD_DIR', create=True):

            configure = Executable('../configure')
            configure("--prefix=%s" % prefix, 
                      "--with-parmetis", 
                      "--with-parmetis-incdir=%s/include" % spec["parmetis"].prefix, 
                      "--with-parmetis-libdir=%s/lib" % spec["parmetis"].prefix,
                      "--disable-mpi",
                      "CC=cc",
                      "CXX=cxx", 
                      "FC=ftn")

            make("everything")
            make("install") 
