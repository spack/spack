from spack import *


class R(Package):
    """
    R is 'GNU S', a freely available language and environment for statistical computing and graphics which provides a
    wide variety of statistical and graphical techniques: linear and nonlinear modelling, statistical tests, time series
    analysis, classification, clustering, etc. Please consult the R project homepage for further information.
    """
    homepage = "https://www.r-project.org"
    url = "http://cran.cnr.berkeley.edu/src/base/R-3/R-3.1.2.tar.gz"

    version('3.2.3', '1ba3dac113efab69e706902810cc2970')
    version('3.2.2', '57cef5c2e210a5454da1979562a10e5b')
    version('3.2.1', 'c2aac8b40f84e08e7f8c9068de9239a3')
    version('3.2.0', '66fa17ad457d7e618191aa0f52fc402e')
    version('3.1.3', '53a85b884925aa6b5811dfc361d73fc4')
    version('3.1.2', '3af29ec06704cbd08d4ba8d69250ae74')

    variant('external-lapack', default=False, description='Links to externally installed BLAS/LAPACK')

    # Virtual dependencies
    depends_on('blas', when='+external-lapack')
    depends_on('lapack', when='+external-lapack')

    # Concrete dependencies
    depends_on('readline')
    depends_on('ncurses')
    depends_on('icu')
    depends_on('glib')
    depends_on('zlib')
    depends_on('libtiff')
    depends_on('jpeg')
    depends_on('cairo')
    depends_on('pango')
    depends_on('freetype')
    depends_on('tcl')
    depends_on('tk')

    def install(self, spec, prefix):
        options = ['--prefix=%s' % prefix,
                   '--enable-R-shlib',
                   '--enable-BLAS-shlib']
        if '+external-lapack' in spec:
            options.extend(['--with-blas', '--with-lapack'])

        configure(*options)
        make()
        make('install')
