from spack import *
from spack.util.environment import *

class Apex(Package):
    homepage = "http://github.com/khuck/xpress-apex"
    url      = "http://github.com/khuck/xpress-apex/archive/v0.1.tar.gz"

    version('0.1', '8b95f0c0313da1575960d3ad69f18e75')

    depends_on("binutils+libiberty")
    depends_on("boost@1.54:")
    depends_on("cmake@2.8.12:")
    depends_on("activeharmony@4.5:")
    depends_on("ompt-openmp")

    def install(self, spec, prefix):

        path=get_path("PATH")
        path.remove(spec["binutils"].prefix.bin)
        path_set("PATH", path)
        with working_dir("build", create=True):
            cmake('-DBOOST_ROOT=%s' % spec['boost'].prefix,
                '-DUSE_BFD=TRUE', 
                '-DBFD_ROOT=%s' % spec['binutils'].prefix,
                '-DUSE_ACTIVEHARMONY=TRUE', 
                '-DACTIVEHARMONY_ROOT=%s' % spec['activeharmony'].prefix,
                '-DUSE_OMPT=TRUE', 
                '-DOMPT_ROOT=%s' % spec['ompt-openmp'].prefix,
                '..', *std_cmake_args)
            make()
            make("install")
