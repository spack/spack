from spack import *

class Openblas(Package):
    """OpenBLAS: An optimized BLAS library"""
    homepage = "http://www.openblas.net"
    url      = "http://github.com/xianyi/OpenBLAS/archive/v0.2.15.tar.gz"

    version('0.2.15', 'b1190f3d3471685f17cfd1ec1d252ac9')

    variant('ilp64', default=False, description="Also support 64-bit indices (i.e. using int64_t or integer*8 to describe array sizes)")

    depends_on('objconv', '+ilp64')

    # virtual dependency
    provides('blas')
    provides('lapack')

    def install(self, spec, prefix):
        make('clean')
        make('libs', 'netlib', 'shared', 'CC=cc', 'FC=f77')
        make('install', "PREFIX=%s" % prefix)

        if spec.satisfies("+ilp64"):
            # Using "64_" as suffix looks a bit strange, but has been set as
            # standard by Julia, and has been picked up by Fedora
            make('clean')
            make('libs', 'netlib', 'shared', 'CC=cc', 'FC=f77',
                'INTERFACE64=1', 'SYMBOLSUFFIX=64_')
            make('install', "PREFIX=%s" % prefix,
                'INTERFACE64=1', 'SYMBOLSUFFIX=64_')

        # Blas virtual package should provide blas.a and libblas.a
        with working_dir(prefix.lib):
            symlink('libopenblas.a', 'blas.a')
            symlink('libopenblas.a', 'libblas.a')
