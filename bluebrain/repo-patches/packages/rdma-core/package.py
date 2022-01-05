from spack import *
from spack.pkg.builtin.rdma_core import RdmaCore as BuiltinRdmaCore


class RdmaCore(BuiltinRdmaCore):
    def patch(self):
        filter_file(
            r'NAMES rst2man',
            'NAMES rst2man.py rst2man',
            'buildlib/Findrst2man.cmake'
        )
