from spack import *

class Modele(CMakePackage):
    """GISS GCM"""

    homepage = "http://www.giss.nasa.gov/tools/modelE"
    url = "http://none"

    # ModelE has no valid versions.
    # This must be built with "spack spconfig" in a local repo
    version('local', '68673158b46b6e88aea6bc4595444adb')

    # More variants will come from the rundeck
    variant('traps',
        default=False, description='Compile with traps, for debugging')
    variant('fexception', default=False,
        description='Use the FException library, for getting good stack traces.')
    variant('debug', default=True,
        description='Use RelWithDebInfo for CMAKE_BUILD_TYPE')
    variant('ic', default=False,
        description='Build init_cond directory')
    variant('diags', default=False,
        description='Build mk_diags directory.')
    variant('aux', default=False,
        description='Build aux directory')
    variant('mpi', default=True,
        description='Build parallel version with MPI')
    variant('pnetcdf', default=True,
        description='Link with the PNetCDF library; required for some rundecks.')

    # Build dependencies
    depends_on('m4')

    # Link dependencies
    depends_on('mpi')
    depends_on('netcdf-fortran')
    depends_on('fexception', when='+fexception')
    depends_on('everytrace', when='+everytrace')
    depends_on('parallel-netcdf+fortran~cxx', when='+pnetcdf')
    # depends_on('netcdf-cxx', when='+pnetcdf')

    # Run dependencies

    def configure_args(self):
        spec = self.spec
        return [
            '-DCMAKE_BUILD_TYPE=%s' % ('Debug' if '+debug' in spec else 'Release'),
            '-DCOMPILE_WITH_TRAPS=%s' % ('YES' if '+traps' in spec else 'NO'),
            '-DCOMPILE_IC=%s' % ('YES' if '+ic' in spec else 'NO'),
            '-DCOMPILE_DIAGS=%s' % ('YES' if '+diags' in spec else 'NO'),
            '-DCOMPILE_AUX=%s' % ('YES' if '+aux' in spec else 'NO'),
            '-DMPI=%s' % ('YES' if '+mpi' in spec else 'NO'),
            '-DUSE_PNETCDF=%s' % ('YES' if '+pnetcdf' in spec else 'NO'),
            '-DUSE_FEXCEPTION=%s' % ('YES' if '+fexception' in spec else 'NO'),
            '-DUSE_EVERYTRACE=%s' % ('YES' if '+everytrace' in spec else 'NO')]


#    def setup_environment(self, spack_env, env):
#        """Add <prefix>/bin to the module; this is not the default if we
#        extend python."""
#        env.prepend_path('PATH', join_path(self.prefix, 'bin'))
