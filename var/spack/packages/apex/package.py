from spack import *
from spack.util.environment import *

class Apex(Package):
    homepage = "http://github.com/khuck/xpress-apex"
    #url      = "http://github.com/khuck/xpress-apex/archive/v0.1-release-candidate.tar.gz"
    url      = "http://github.com/khuck/xpress-apex"

    #version('0.1', '6e039c224387348296739f6bf360d081')
    version('master', branch='master', git='https://github.com/khuck/xpress-apex.git')

    depends_on("binutils+libiberty")
    depends_on("boost@1.54:")
    depends_on("cmake@2.8.12:")
    depends_on("activeharmony@4.5:")

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
                '..', *std_cmake_args)
            make()
            make("install")
