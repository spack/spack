from spack import *

class Swan(MakefilePackage):
    """SWAN is a third-generation wave model, developed at Delft 
    University of Technology, that computes random, short-crested
     wind-generated waves in coastal regions and inland waters. 
    For more information about SWAN, see a short overview of model 
    features. This list reflects on the scientific relevance of 
    the development of SWAN."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://swanmodel.sourceforge.net/"
    url      = "https://cfhcable.dl.sourceforge.net/project/swanmodel/swan/41.31/swan4131.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers = ['lhxone']

    version('4131', sha256='cd3ba1f0d79123f1b7d42a43169f07575b59b01e604c5e66fbc09769e227432e')

    depends_on('mpich', type = 'build')
    depends_on('netcdf-fortran', type = ('build', 'run'))
    depends_on('libfabric', type = ('run'))

    def edit(self, spec, prefix):
        env['FC'] = 'gfortran'
        makefile = FileFilter('platform.pl')
        makefile.filter('F90_MPI = .*', 'F90_MPI = mpifort\\n";')
        makefile.filter('NETCDFROOT =', 'NETCDFROOT = {0}'.format(spec['netcdf-fortran'].prefix))

    def build(self, spec, prefix):
        make('config')
        make('mpi')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('*.exe', prefix.bin)