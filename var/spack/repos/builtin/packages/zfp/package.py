from spack import *

class Zfp(Package):
    """zfp is an open source C library for compressed floating-point arrays that supports
       very high throughput read and write random acces, target error bounds or bit rates.
       Although bit-for-bit lossless compression is not always possible, zfp is usually
       accurate to within machine epsilon in near-lossless mode, and is often orders of
       magnitude more accurate than other lossy compressors.
    """

    homepage = "http://computation.llnl.gov/projects/floating-point-compression"
    url      = "http://computation.llnl.gov/projects/floating-point-compression/download/zfp-0.5.0.tar.gz"

    version('0.5.0', '2ab29a852e65ad85aae38925c5003654')

    def install(self, spec, prefix):
        make("shared")

        # No install provided
        mkdirp(prefix.lib)
        mkdirp(prefix.include)
        install('lib/libzfp.so', prefix.lib)
        install('inc/zfp.h', prefix.include)
        install('inc/types.h', prefix.include)
        install('inc/bitstream.h', prefix.include)
        install('inc/system.h', prefix.include)
