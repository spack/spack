from spack.package import *
from spack.pkg.builtin.singularityce import Singularityce as BuiltinSingularityce


class Singularityce(BuiltinSingularityce):
    __doc__ = BuiltinSingularityce.__doc__

    depends_on('glib@2', type=('build', 'run'))
