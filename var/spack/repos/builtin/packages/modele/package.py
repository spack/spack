from spack import *

class Modele(CMakePackage):
    """GISS GCM"""

    homepage = "http://www.giss.nasa.gov/tools/modelE"
    url = "http://none"

    # ModelE has no valid versions.
    # This must be built with "spack spconfig" in a local repo
    version('landice',
        git='simplex.giss.nasa.gov:/giss/gitrepo/modelE.git',
        branch='landice')

    # More variants will come from the rundeck
    variant('traps',
        default=False, description='Compile with traps, for debugging')
    variant('fexception', default=False,
        description='Use the FException library, for getting good stack traces.')
    variant('debug', default=False,
        description='Use Debug for CMAKE_BUILD_TYPE')
    variant('model', default=True,
        description='Build main model')
    variant('ic', default=False,
        description='Build init_cond directory')
    variant('diags', default=False,
        description='Build mk_diags directory.')
    variant('aux', default=False,
        description='Build aux directory')
    variant('mpi', default=True,
        description='Build parallel version with MPI')
    variant('pnetcdf', default=False,
        description='Link with the PNetCDF library; required for some rundecks.')
    variant('glint2', default=False,
        description='Link with the Glint2 Ice Model Coupler')
    variant('everytrace', default=True,
        description='Link to enhanced staktrace capabilities')
    variant('mods', default=False,
        description='Install .mod files')
#    variant('tests', default=True,
#        description='Build unit tests')

    # Build dependencies
    depends_on('m4')

    # Link dependencies
    depends_on('mpi')
    #depends_on('pfunit+mpi', when='+tests')
    depends_on('netcdf-fortran')
    depends_on('fexception', when='+fexception')
    depends_on('everytrace+fortran+mpi', when='+everytrace')
    depends_on('parallel-netcdf+fortran~cxx', when='+pnetcdf')
    depends_on('glint2+coupler', when='+glint2')

    # depends_on('netcdf-cxx', when='+pnetcdf')

    # Run dependencies

    def configure_args(self):
        spec = self.spec
        return [
            '-DCMAKE_BUILD_TYPE=%s' % ('Debug' if '+debug' in spec else 'Release'),
            '-DCOMPILE_WITH_TRAPS=%s' % ('YES' if '+traps' in spec else 'NO'),
            '-DCOMPILE_MODEL=%s' % ('YES' if '+model' in spec else 'NO'),
            '-DCOMPILE_IC=%s' % ('YES' if '+ic' in spec else 'NO'),
            '-DCOMPILE_DIAGS=%s' % ('YES' if '+diags' in spec else 'NO'),
            '-DCOMPILE_AUX=%s' % ('YES' if '+aux' in spec else 'NO'),
            '-DMPI=%s' % ('YES' if '+mpi' in spec else 'NO'),
            '-DUSE_PNETCDF=%s' % ('YES' if '+pnetcdf' in spec else 'NO'),
            '-DUSE_FEXCEPTION=%s' % ('YES' if '+fexception' in spec else 'NO'),
            '-DUSE_EVERYTRACE=%s' % ('YES' if '+everytrace' in spec else 'NO'),
            '-DUSE_GLINT2=%s' % ('YES' if '+glint2' in spec else 'NO'),
            '-DINSTALL_MODS=%s' % ('YES' if '+mods' in spec else 'NO')]
#            '-DWITH_PFUNIT=%s' % ('YES' if '+tests' in spec else 'NO')]


    def setup_environment(self, spack_env, env):
        """Add <prefix>/bin to the module; this is not the default if we
        extend python."""
        env.prepend_path('PATH', join_path(self.prefix, 'bin'))
