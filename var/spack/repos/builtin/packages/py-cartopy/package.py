# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCartopy(PythonPackage):
    """Cartopy - a cartographic python library with matplotlib support."""

    homepage = "https://scitools.org.uk/cartopy/docs/latest/"
    url      = "https://github.com/SciTools/cartopy/archive/v0.18.0.tar.gz"

    maintainers = ['adamjstewart']

    # Tests require extra dependencies, skip them in 'import_modules'
    import_modules = [
        'cartopy', 'cartopy.sphinxext', 'cartopy.io', 'cartopy.geodesic',
        'cartopy.examples', 'cartopy.mpl', 'cartopy.feature'
    ]

    version('0.18.0', sha256='493ced4698361ffabec1a213d2b711dc836117242c304f3b93f5406182fd8bc2')
    version('0.17.0', sha256='137642e63952404ec0841fa0333ad14c58fbbf19cca2a5ac6a38498c4b4998fb')
    version('0.16.0', sha256='cadf62434492c965220b37f0548bc58180466ad6894a1db57dbc51cd43467e5c')

    variant('epsg', default=False, description='Add support for epsg.io')
    variant('ows', default=False, description='Add support for Open Geospatial Consortium (OGC) web service')
    variant('plotting', default=False, description='Add plotting functionality')

    # https://scitools.org.uk/cartopy/docs/latest/installing.html#installing
    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools@0.7.2:', type='build')
    depends_on('py-cython@0.28:',    type='build')
    depends_on('py-numpy@1.10.0:',  type=('build', 'run'))
    depends_on('py-shapely@1.5.6:', type=('build', 'run'))
    depends_on('py-pyshp@1.1.4:',   type=('build', 'run'))
    depends_on('py-six@1.3.0:',     type=('build', 'run'))
    depends_on('py-futures', when='^python@:2', type=('build', 'run'))
    depends_on('geos@3.3.3:')
    depends_on('proj@4.9:5', when='@:0.16.0')
    depends_on('proj@4.9:7', when='@0.17.0:')

    # Optional dependecies
    depends_on('py-pyepsg@0.4.0:',     type=('build', 'run'), when='+epsg')
    depends_on('py-owslib@0.8.11:',    type=('build', 'run'), when='+ows')
    depends_on('pil@1.7.8:',           type=('build', 'run'), when='+ows')
    depends_on('py-matplotlib@1.5.1:', type=('build', 'run'), when='+plotting')
    depends_on('gdal@1.10.0:+python',  type=('build', 'run'), when='+plotting')
    depends_on('pil@1.7.8:',           type=('build', 'run'), when='+plotting')
    depends_on('py-scipy@0.10:',       type=('build', 'run'), when='+plotting')

    patch('proj6.patch', when='@0.17.0')

    def setup_build_environment(self, env):
        # Needed for `spack install --test=root py-cartopy`
        library_dirs = []
        for dep in self.spec.dependencies(deptype='link'):
            query = self.spec[dep.name]
            library_dirs.extend(query.libs.directories)

        # Cartopy uses ctypes.util.find_library, which searches LD_LIBRARY_PATH
        # Our RPATH logic works fine, but the unit tests fail without this
        libs = ':'.join(library_dirs)
        if self.spec.satisfies('platform=darwin'):
            env.prepend_path('DYLD_FALLBACK_LIBRARY_PATH', libs)
        else:
            env.prepend_path('LD_LIBRARY_PATH', libs)

    # Needed for `spack test run py-cartopy`
    setup_run_environment = setup_build_environment

    # Needed for `spack test run py-foo` where `py-foo` depends on `py-cartopy`
    def setup_dependent_run_environment(self, env, dependent_spec):
        self.setup_build_environment(env)
