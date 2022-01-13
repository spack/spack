from spack import *
from spack.pkg.builtin.openscenegraph import Openscenegraph as BuiltinOpenscenegraph


class Openscenegraph(BuiltinOpenscenegraph):
    depends_on('openexr')
