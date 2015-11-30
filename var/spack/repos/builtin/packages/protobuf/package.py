import os
from spack import *

class Protobuf(Package):
    """Google's data interchange format."""

    homepage = "https://developers.google.com/protocol-buffers"
    url      = "https://github.com/google/protobuf/releases/download/v2.5.0/protobuf-2.5.0.tar.bz2"

    version('2.5.0', 'a72001a9067a4c2c4e0e836d0f92ece4')

    def install(self, spec, prefix):
        configure("--prefix=" + prefix)
        make()
        make("check")
        make("install")
