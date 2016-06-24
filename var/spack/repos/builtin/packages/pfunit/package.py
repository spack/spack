from spack import *
import os

class Pfunit(Package):
    """Regridding/Coupling library for GCM + Ice Sheet Model"""

    homepage = "http://pfunit.sourceforge.net/index.html"
    url = "http://downloads.sourceforge.net/project/pfunit/Source/pFUnit-3.2.7.tar.gz"

    version('3.2.7', '7e994e031c679ed0b446be8b853d5e69')

    version('3.2.7-citibeth', git='git://git.code.sf.net/u/citibeth2/pfunit',
        branch='3.2.7-citibeth')

    depends_on('mpi', when='+mpi')
    depends_on('openmp', when='+openmp')

    # Build dependencies
    depends_on('cmake')
    depends_on('doxygen')

    variant('shared', default=True,
        description='Build shared library in addition to static')
    variant('mpi', default=True,
        description='Test MPI-based programs')
    variant('openmp', default=False,
        description='Test OpenMP-based programs')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            options = std_cmake_args + [
                '-DBUILD_SHARED=%s' % ('YES' if '+shared' in spec else 'NO'),
                '-DMPI=%s' % ('YES' if '+mpi' in spec else 'NO'),
                '-OPENMP=%s' % ('YES' if '+openmp' in spec else 'NO'),
                '-DINSTALL_PATH=%s' % prefix]
            which('cmake')(self.stage.source_path, *options)
#            make('tests')
            make()
            make('install', 'INSTALL_DIR=%s' % prefix)

    def setup_dependent_package(self, module, dspec):
        self.spec.pfunit_prefix = self.prefix

    def setup_environment(self, spack_env, env):
        super(Pfunit, self).setup_environment(spack_env,env)
        env.prepend_path('CPATH', join_path(self.prefix, 'mod'))
        #env.prepend_path('PFUNIT', self.prefix)
