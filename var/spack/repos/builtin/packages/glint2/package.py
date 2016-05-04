from spack import *

class Glint2(CMakePackage):
    """Regridding/Coupling library for GCM + Ice Sheet Model"""

    homepage = "https://github.com/citibeth/icebin"
    url         = "https://github.com/citibeth/icebin/tarball/v0.1.0"

    version('0.1.0', '1c2769a0cb3531e4086b885dc7a6fd27')

    variant('python', default=True, description='Build Python extension (requires Python, Numpy)')
    variant('coupler', default=True, description='Build the GCM coupler (requires MPI)')
    variant('pism', default=False, description='Build coupling link with PISM (requires PISM, PETSc)')

    extends('python', when='+python')

#    depends_on('everytrace')

    depends_on('python@3:', when='+python')
    depends_on('py-cython', when='+python')
    depends_on('py-numpy', when='+python')

    depends_on('cgal')
    depends_on('gmp')
    depends_on('mpfr')

    depends_on('mpi', when='+coupler')
    depends_on('pism@glint2~python', when='+coupler+pism')
    depends_on('petsc', when='+coupler+pism')

    depends_on('boost+filesystem+date_time')
    depends_on('blitz')
    depends_on('netcdf-cxx')
    depends_on('proj')
    depends_on('eigen')
    depends_on('galahad')

    # Build dependencies
    depends_on('cmake')
    depends_on('doxygen')


    # Dummy dependency to work around Spack bug
    depends_on('openblas')

    def configure_args(self):
        spec = self.spec
        return [
            '-DUSE_PYTHON=%s' % ('YES' if '+python' in spec else 'NO'),
            '-DUSE_PISM=%s' % ('YES' if '+pism' in spec else 'NO')]

    def setup_environment(self, spack_env, env):
        """Add <prefix>/bin to the module; this is not the default if we
        extend python."""
        env.prepend_path('PATH', join_path(self.prefix, 'bin'))
