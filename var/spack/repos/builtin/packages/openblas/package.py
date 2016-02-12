from spack import *

class Openblas(Package):
    """OpenBLAS: An optimized BLAS library"""
    homepage = "http://www.openblas.net"
    url      = "http://github.com/xianyi/OpenBLAS/archive/v0.2.15.tar.gz"

    version('0.2.15', 'b1190f3d3471685f17cfd1ec1d252ac9')

    # virtual dependency
    provides('blas')
    provides('lapack')

    def install(self, spec, prefix):
        make('libs', 'netlib', 'shared', 'CC=cc', 'FC=f77')
        make('install', "PREFIX='%s'" % prefix)

        # Blas virtual package should provide blas.a and libblas.a
        with working_dir(prefix.lib):
            symlink('libopenblas.a', 'blas.a')
            symlink('libopenblas.a', 'libblas.a')
            symlink('libopenblas.so', 'libblas.so')

        # Lapack virtual package should provide liblapack.a
        with working_dir(prefix.lib):
            symlink('libopenblas.a', 'liblapack.a')
            symlink('libopenblas.so', 'liblapack.so')
