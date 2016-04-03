from spack import *

class PyNumpy(Package):
    """NumPy is the fundamental package for scientific computing with Python.
    It contains among other things: a powerful N-dimensional array object,
    sophisticated (broadcasting) functions, tools for integrating C/C++ and
    Fortran code, and useful linear algebra, Fourier transform, and random
    number capabilities"""
    homepage = "http://www.numpy.org/"
    url      = "https://pypi.python.org/packages/source/n/numpy/numpy-1.9.1.tar.gz"

    version('1.11.0', 'bc56fb9fc2895aa4961802ffbdb31d0b')
    version('1.10.4', 'aed294de0aa1ac7bd3f9745f4f1968ad')
    version('1.9.2',  'a1ed53432dbcd256398898d35bc8e645')
    version('1.9.1',  '78842b73560ec378142665e712ae4ad9')


    variant('blas',   default=True)
    variant('lapack', default=True)

    extends('python')
    depends_on('binutils')
    depends_on('py-nose')
    depends_on('blas',   when='+blas')
    depends_on('lapack', when='+lapack')

    def install(self, spec, prefix):
        libraries    = []
        library_dirs = []

        if '+blas' in spec:
            libraries.append('blas')
            library_dirs.append(spec['blas'].prefix.lib)
        if '+lapack' in spec:
            libraries.append('lapack')
            library_dirs.append(spec['lapack'].prefix.lib)

        if '+blas' in spec or '+lapack' in spec:
            with open('site.cfg', 'w') as f:
                f.write('[DEFAULT]\n')
                f.write('libraries=%s\n'    % ','.join(libraries))
                f.write('library_dirs=%s\n' % ':'.join(library_dirs))

        python('setup.py', 'install', '--prefix=%s' % prefix)

