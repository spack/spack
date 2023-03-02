from spack.package import *
from spack.pkg.builtin.node_js import NodeJs as BuiltinNodeJs


class NodeJs(BuiltinNodeJs):
    __doc__ = BuiltinNodeJs.__doc__

    version(
        "18.12.1",
        sha256="ba8174dda00d5b90943f37c6a180a1d37c861d91e04a4cb38dc1c0c74981c186",
        preferred=True,
    )
