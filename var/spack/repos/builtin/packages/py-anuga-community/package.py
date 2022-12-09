#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-anuga-community
#
# You can edit this file again by typing:
#
#     spack edit py-anuga-community
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyAnugaCommunity(PythonPackage):
    """ANUGA (pronounced "AHnooGAH") is open-source software for the simulation
    of the shallow water equation, in particular it can be used to model
    tsunamis and floods."""
    homepage = "https://github.com/GeoscienceAustralia/anuga_core"
    git      = "https://github.com/anuga-community/anuga_core.git"
    url      = "https://github.com/anuga-community/anuga_core.git"

    maintainers = ['samcom12, jayashripawar']
    version('main',  branch='main', preferred=True)
    version('3.0.2', url='https://github.com/anuga-community/anuga_core/archive/refs/tags/3.0.2.tar.gz', sha256='81f291787518b21782ef54c781ecdfcd1efdfd02d2519492826acaeed7165cfe')


    variant('mpi', default=True, description='Install anuga_parallel')
    #variant('openmp', default=True, description='Install with OpenMP support')

    depends_on('python@3.7:3.11', type=('build', 'link', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('gdal', type=('build', 'run'))
    depends_on('py-cython', type=('build', 'run'))
    depends_on('py-pytest', type=('build', 'run'))
    depends_on('py-netcdf4', type=('build', 'run'))
    depends_on('py-dill', type=('build', 'run'))
    depends_on('py-future', type=('build', 'run'))
    depends_on('gdal', type=('build', 'run'))
    depends_on('py-pyproj', type=('build', 'run'))
    depends_on('py-ipython', type=('build', 'run'))
    depends_on('py-mpi4py', type=('build', 'run'))
    depends_on('py-meshpy', type=('build', 'run'))
    depends_on('py-utm', type=('build'))
    #depends_on('py-backport.zoneinfo', type=('build', 'run'))  #needs to be added for latest version
    depends_on('py-pmw', type=('build', 'run'))
    depends_on('py-pymetis', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('triangle', type=('build', 'run'))
    depends_on('py-openpyxl', type=('build', 'run'))
    depends_on('py-xarray', type=('build', 'run'))
    depends_on('py-xlrd', type=('build', 'run'))
    depends_on('py-pytz', type=('build', 'run'))
    depends_on('py-tzdata', type=('build', 'run'))
    depends_on('mpi', type=('test',  'run'))

    def setup_run_environment(self, env):
        if self.run_tests:
            env.prepend_path('PATH', self.spec['mpi'].prefix.bin)

    install_time_test_callbacks = ['test', 'installtest']

    def installtest(self):
        python('runtests.py', '--no-build')
