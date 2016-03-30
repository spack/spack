from spack import *

class Openjpeg(Package):
    """
    OpenJPEG is an open-source JPEG 2000 codec written in C language.
    It has been developed in order to promote the use of JPEG 2000, a
    still-image compression standard from the Joint Photographic
    Experts Group (JPEG).
    Since April 2015, it is officially recognized by ISO/IEC and
    ITU-T as a JPEG 2000 Reference Software.
    """
    homepage = "https://github.com/uclouvain/openjpeg"
    url      = "https://github.com/uclouvain/openjpeg/archive/version.2.1.tar.gz"

    version('2.1'  , '3e1c451c087f8462955426da38aa3b3d')
    version('2.0.1', '105876ed43ff7dbb2f90b41b5a43cfa5')
    version('2.0'  , 'cdf266530fee8af87454f15feb619609')
    version('1.5.2', '545f98923430369a6b046ef3632ef95c')
    version('1.5.1', 'd774e4b5a0db5f0f171c4fc0aabfa14e')


    def install(self, spec, prefix):
        cmake('.', *std_cmake_args)

        make()
        make("install")
