from spack import *


class LibmmtfCpp(CMakePackage):
    """The macromolecular transmission format (MMTF) is a binary encoding of biological structures. This repository holds the C++-03 compatible API, encoding and decoding libraries."""

    homepage = "https://github.com/rcsb/mmtf-cpp"
    url      = "https://github.com/rcsb/mmtf-cpp/archive/v1.0.0.tar.gz"

    version('1.0.0', sha256='881f69c4bb56605fa63fd5ca50842facc4947f686cbf678ad04930674d714f40')

    depends_on('msgpack-c')
