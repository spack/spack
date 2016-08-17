from spack import *

class ModeleUtils(CMakePackage):
    """Utities for GISS GCM"""

    homepage = "http://www.giss.nasa.gov/tools/modelE"
    url = "http://none"

    # ModelE has no valid versions.
    # This must be built with "spack spconfig" in a local repo
    version('cmake',
        git='simplex.giss.nasa.gov:/giss/gitrepo/modelE.git',
        branch='cmake')

    variant('ic', default=True,
        description='Build init_cond directory')
    variant('diags', default=True,
        description='Build mk_diags directory.')
    variant('aux', default=True,
        description='Build aux directory')

    # Build dependencies
    depends_on('m4')
    depends_on('cmake')

    # Link dependencies
    depends_on('netcdf-fortran')

    # depends_on('netcdf-cxx', when='+pnetcdf')

    # Run dependencies

    def configure_args(self):
        spec = self.spec
        return [
            '-DCMAKE_BUILD_TYPE=%s' % ('Debug' if '+debug' in spec else 'Release'),
            '-DCOMPILE_WITH_TRAPS=NO',
            '-DCOMPILE_MODEL=NO',
            '-DCOMPILE_IC=%s' % ('YES' if '+ic' in spec else 'NO'),
            '-DCOMPILE_DIAGS=%s' % ('YES' if '+diags' in spec else 'NO'),
            '-DCOMPILE_AUX=%s' % ('YES' if '+aux' in spec else 'NO'),
            '-DMPI=NO',
            '-DUSE_PNETCDF=NO',
            '-DUSE_FEXCEPTION=NO',
            '-DUSE_EVERYTRACE=NO',
            '-DUSE_GLINT2=NO']


    def setup_environment(self, spack_env, env):
        """Add <prefix>/bin to the module"""
        env.prepend_path('PATH', join_path(self.prefix, 'bin'))
