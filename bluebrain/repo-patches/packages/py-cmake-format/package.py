# from spack.package import *
from spack.pkg.builtin.py_cmake_format import PyCmakeFormat as BuiltinPyCmakeFormat


class PyCmakeFormat(BuiltinPyCmakeFormat):
    __doc__ = BuiltinPyCmakeFormat.__doc__

    # the tarball filename format changed starting with 0.6.12
    # Unfortunately, those tarballs are also broken - 0.6.11 is the last working version at the time of writing
    # pypi = "cmake-format/cmake-format-0.6.12.tar.gz"
    pypi = "cmake-format/cmake_format-0.6.9.tar.gz"

    version("0.6.11", sha256="aa3d0e6156bcd4ae8fbd630ccb1d4995179b37b1b31923f2eb53764104da75f3")

    depends_on('py-pyyaml', type=('run'))
