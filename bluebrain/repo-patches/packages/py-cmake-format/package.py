# from spack.package import *
from spack.pkg.builtin.py_cmake_format import PyCmakeFormat as BuiltinPyCmakeFormat


class PyCmakeFormat(BuiltinPyCmakeFormat):
    __doc__ = BuiltinPyCmakeFormat.__doc__

    pypi = "cmake-format/cmake-format-0.6.9.tar.gz"

    version("0.6.13", sha256="1a48b779067ecca68c498691d07d5c9d3df9803a7e0c5b641128fa6efe5ae489")
    version("0.6.12", sha256="fd6e95c6f4f44fe7eb24cda118ba7e3e1a61997c24127ab5e7ca414940e07e5a")

    depends_on('py-pyyaml', type=('run'))
