from spack import *
from spack.pkg.builtin.gobject_introspection import GobjectIntrospection as BuiltinGobjectIntrospection


class GobjectIntrospection(BuiltinGobjectIntrospection):
    depends_on("glib@2.56.1:", when="@1.56.1:")
