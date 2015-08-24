from spack import *

class PyNumpy(Package):
    """array processing for numbers, strings, records, and objects."""
    homepage = "https://pypi.python.org/pypi/numpy"
    url      = "https://pypi.python.org/packages/source/n/numpy/numpy-1.9.1.tar.gz"

    version('1.9.1', '78842b73560ec378142665e712ae4ad9')
    version('1.9.2', 'a1ed53432dbcd256398898d35bc8e645')
    
    extends('python')
    depends_on('py-nose')
    depends_on('netlib-blas+fpic')
    depends_on('netlib-lapack+shared')

    def patch(self):
        filter_file(
            "possible_executables = \['(gfortran|g77|ifort|efl)",
            "possible_executables = ['fc",
            "numpy/distutils/fcompiler/gnu.py",
            "numpy/distutils/fcompiler/intel.py")

    def install(self, spec, prefix):
        with open('site.cfg', 'w') as f:
            f.write('[DEFAULT]\n')
            f.write('libraries=lapack,blas\n')
            f.write('library_dirs=%s/lib:%s/lib\n' % (spec['blas'].prefix, spec['lapack'].prefix))
        python('setup.py', 'install', '--prefix=%s' % prefix)
