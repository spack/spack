from spack import *
import sys

class Openblas(Package):
    """OpenBLAS: An optimized BLAS library"""
    homepage = "http://www.openblas.net"
    url      = "http://github.com/xianyi/OpenBLAS/archive/v0.2.15.tar.gz"

    version('0.2.17', '664a12807f2a2a7cda4781e3ab2ae0e1')
    version('0.2.16', 'fef46ab92463bdbb1479dcec594ef6dc')
    version('0.2.15', 'b1190f3d3471685f17cfd1ec1d252ac9')

    # virtual dependency
    provides('blas')
    provides('lapack')

    def install(self, spec, prefix):
        extra=[]
        if spec.satisfies('@0.2.16'):
            extra.extend([
                'BUILD_LAPACK_DEPRECATED=1' # fix missing _dggsvd_ and _sggsvd_
            ])

        make('libs', 'netlib', 'shared', 'CC=cc', 'FC=f77',*extra)
        make("tests")
        make('install', "PREFIX='%s'" % prefix)

        lib_dsuffix = 'dylib' if sys.platform == 'darwin' else 'so'
        # Blas virtual package should provide blas.a and libblas.a
        with working_dir(prefix.lib):
            symlink('libopenblas.a', 'blas.a')
            symlink('libopenblas.a', 'libblas.a')
            symlink('libopenblas.%s' % lib_dsuffix, 'libblas.%s' % lib_dsuffix)

        # Lapack virtual package should provide liblapack.a
        with working_dir(prefix.lib):
            symlink('libopenblas.a', 'liblapack.a')
            symlink('libopenblas.%s' % lib_dsuffix, 'liblapack.%s' % lib_dsuffix)
