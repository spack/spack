from spack import *

class Magma(Package):
    """The MAGMA project aims to develop a dense linear algebra library
    similar to LAPACK but for heterogeneous/hybrid architectures,
    starting with current "Multicore+GPU" systems.
    """

    homepage = "http://icl.cs.utk.edu/magma/"
    base_url = "http://icl.cs.utk.edu/projectsfiles/magma/downloads/"

    version('2.2.0', '6c1ebf4cdf63eb302ff6258ff8c49217')

    depends_on('cmake', type='build')
    depends_on('lapack')

    patch('ibm-xl.patch', when='%xl')
    patch('ibm-xl.patch', when='%xl_r')

    def url_for_version(self, version):
        return '%s/magma-%s.tar.gz' % (Magma.base_url, version)

    def install(self, spec, prefix):

        options = []

        options.extend([
            '-DCMAKE_INSTALL_PREFIX=%s' % prefix,
            '-DUSE_FORTRAN=yes',
            '-DCMAKE_Fortran_FLAGS=-qfixed',
            '-DLAPACK_LIBRARIES=%s;%s' % (spec['blas'].blas_libs,spec['lapack'].lapack_libs)
        ])

        with working_dir('spack-build', create=True):
            cmake('..', *options)
            make()
            make('install')

