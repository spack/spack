from spack.package import *
from spack.pkg.builtin.gobject_introspection import (
    GobjectIntrospection as BuiltinGobjectIntrospection,
)


class GobjectIntrospection(BuiltinGobjectIntrospection):
    __doc__ = BuiltinGobjectIntrospection.__doc__

    depends_on("glib@2.56.1:", when="@1.56.1:")
