from spack import *

class Relion(CMakePackage):
    """RELION (for REgularised LIkelihood OptimisatioN, pronounce rely-on) is a
    stand-alone computer program that employs an empirical Bayesian approach to
    refinement of (multiple) 3D reconstructions or 2D class averages in
    electron cryo-microscopy (cryo-EM)."""

    homepage = "http://http://www2.mrc-lmb.cam.ac.uk/relion"
    url      = "https://github.com/3dem/relion/archive/2.0.3.tar.gz"

    version('2.0.3', 'c61be5ef00848806278b341f43893f5d')

    variant('gui', default=True, description="build the gui")
    variant('cuda', default=False, description="enable compute on gpu")
    variant('double', default=False, description="double precision (cpu) code")
    variant('double-gpu', default=False, description="double precision (gpu) code")

    depends_on('mpi')
    depends_on('fftw+float+double')
    depends_on('fltk', when='+gui')
    depends_on('cuda', when='+cuda')

    def cmake_args(self):
        args = [
            '-DCMAKE_C_FLAGS=-g',
            '-DCMAKE_CXX_FLAGS=-g',
            '-DGUI=%s' % ('on' if '+gui' in self.spec else 'off'),
            '-DDoublePrec_CPU=%s' % ('on' if '+double' in self.spec else 'off'),
            '-DDoublePrec_GPU=%s' % ('on' if '+double-gpu' in self.spec else 'off'),
            ]
        if '+cuda' in self.spec:
            args += [
                '-DCUDA=on',
                '-DCUFFT=on',
                ]
        return args

