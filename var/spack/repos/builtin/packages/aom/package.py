from spack import *

class Aom(CMakePackage):
    """Alliance for Open Media"""
    homepage = "https://aomedia.googlesource.com/aom"
    git      = "https://aomedia.googlesource.com/aom"
    version('v1.0.0-errata1', commit='29d8ce4836630df5cc7ab58f1afc4836765fc212')
    version('1.0.0', commit='d14c5bb4f336ef1842046089849dee4a301fbbf0')
    depends_on('binutils', type='build')
    depends_on('cmake', type='build')
    depends_on('gmake', type='build')
    depends_on('yasm')
    depends_on('nasm')

    def cmake_args(self):
        args=[]
        args.append('-DBUILD_SHARED_LIBS=ON')
        return args

