from spack import *

class PyScipy(Package):
    """Scientific Library for Python."""
    homepage = "http://www.scipy.org/"
    url      = "https://pypi.python.org/packages/source/s/scipy/scipy-0.15.0.tar.gz"

    version('0.17.0', '5ff2971e1ce90e762c59d2cd84837224')
    version('0.15.1', 'be56cd8e60591d6332aac792a5880110')
    version('0.15.0', '639112f077f0aeb6d80718dc5019dc7a')

    extends('python')
    depends_on('binutils')
    depends_on('py-nose')
    depends_on('py-numpy+blas+lapack')

    def install(self, spec, prefix):
        if 'atlas' in spec:
            # libatlas.so actually isn't always installed, but this
            # seems to make the build autodetect things correctly.
            env['ATLAS'] = join_path(spec['atlas'].prefix.lib, 'libatlas.' + dso_suffix)
        else:
            blas_spec = spec['blas']
            try:
                env['BLAS']   = blas_spec.blas_shared_lib
            except AttributeError:
                # This installation has not shared lib; use static
                env['BLAS']   = blas_spec.blas_static_lib

            lapack_spec = spec['lapack']
            try:
                env['LAPACK']   = lapack_spec.lapack_shared_lib
            except AttributeError:
                # This installation has not shared lib; use static
                env['LAPACK']   = lapack_spec.lapack_static_lib

        python('setup.py', 'install', '--prefix=%s' % prefix)
