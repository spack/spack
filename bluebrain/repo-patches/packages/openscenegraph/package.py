from spack import *
from spack.pkg.builtin.openscenegraph import Openscenegraph as BuiltinOpenscenegraph


class Openscenegraph(BuiltinOpenscenegraph):
    __doc__ = BuiltinOpenscenegraph.__doc__

    depends_on('openexr')
