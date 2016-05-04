from spack import *

class Icebin(CMakePackage):
    """Regridding/Coupling library for GCM + Ice Sheet Model"""

    homepage = "https://github.com/citibeth/icebin"
    url         = "https://github.com/citibeth/icebin/tarball/v0.1.0"

    version('0.1.4', '5c8ecd778255f2972c0caa3a9f5d82ea')
    version('0.1.3', '98d9b28ef8f8a145a7eed2cb1e92e7e4')
    version('0.1.2', '68673158b46b6e88aea6bc4595444adb')
    version('0.1.1', '986b8b51a2564f9c52156a11642e596c')
    version('0.1.0', '1c2769a0cb3531e4086b885dc7a6fd27')

    variant('everytrace', default=False, description='Report errors through Everytrace (requires Everytrace)')
    variant('python@3:', default=True, description='Build Python extension (requires Python, Numpy)')
    variant('gridgen', default=True, description='Build grid generators (requires CGAL, GMP, MPFR)')
    variant('coupler', default=True, description='Build the GCM coupler (requires MPI)')
    variant('pism', default=False, description='Build coupling link with PISM (requires PISM, PETSc)')

    extends('python', when='+python')

    depends_on('everytrace', when='+everytrace')

    depends_on('python', when='+python')
    depends_on('py-cython', when='+python')
    depends_on('py-numpy', when='+python')

    depends_on('cgal', when='+gridgen')
    depends_on('gmp', when='+gridgen')
    depends_on('mpfr', when='+gridgen')

    depends_on('mpi', when='+coupler')
    depends_on('pism~python', when='+coupler+pism')
    depends_on('petsc', when='+coupler+pism')

    depends_on('boost+filesystem+date_time')
    depends_on('blitz')
    depends_on('netcdf-cxx4')
    depends_on('ibmisc+proj+blitz+netcdf+boost+udunits2+python')
    depends_on('proj')
    depends_on('eigen')


    # Build dependencies
    depends_on('cmake')
    depends_on('doxygen')

    def configure_args(self):
        spec = self.spec
        return [
            '-DUSE_EVERYTRACE=%s' % ('YES' if '+everytrace' in spec else 'NO'),
            '-DBUILD_PYTHON=%s' % ('YES' if '+python' in spec else 'NO'),
            '-DBUILD_GRIDGEN=%s' % ('YES' if '+gridgen' in spec else 'NO'),
            '-DBUILD_COUPLER=%s' % ('YES' if '+coupler' in spec else 'NO'),
            '-DUSE_PISM=%s' % ('YES' if '+pism' in spec else 'NO')]

    def setup_environment(self, spack_env, env):
        """Add <prefix>/bin to the module; this is not the default if we
        extend python."""
        env.prepend_path('PATH', join_path(self.prefix, 'bin'))
