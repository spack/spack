from spack import *

class PyNumpy(Package):
    """array processing for numbers, strings, records, and objects."""
    homepage = "https://pypi.python.org/pypi/numpy"
    url      = "https://pypi.python.org/packages/source/n/numpy/numpy-1.9.1.tar.gz"

    version('1.9.1', '78842b73560ec378142665e712ae4ad9')
    version('1.9.2', 'a1ed53432dbcd256398898d35bc8e645')

    variant('blas', default=True)
    variant('fortran', default=True)

    extends('python')
    depends_on('py-nose')
    depends_on('netlib-blas+fpic', when='+blas')
    depends_on('netlib-blas+fpic+fortran', when='+blas+fortran')
    depends_on('netlib-lapack+shared', when='+blas')

    def install(self, spec, prefix):
        args = []
        if '+blas' in spec:
            with open('site.cfg', 'w') as f:
                f.write('[DEFAULT]\n')
                f.write('libraries=lapack,blas\n')
                f.write('library_dirs=%s/lib:%s/lib\n' % (spec['blas'].prefix, spec['lapack'].prefix))
        if '+fortran' not in spec:
            # Numpy's build system complains that 'no' is not a compiler, but
            # it is not fatal; other values are not fatal.
            args.append('--fcompiler=no')
        python('setup.py', 'install', '--prefix=%s' % prefix, *args)
