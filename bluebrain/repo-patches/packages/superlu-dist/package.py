from spack import *
from spack.pkg.builtin.superlu_dist import SuperluDist as BuiltinSuperluDist


class SuperluDist(BuiltinSuperluDist):
    depends_on('parmetis~int64', when='~int64')
    depends_on('parmetis+int64', when='+int64')
    depends_on('metis@5:~int64', when='~int64')
    depends_on('metis@5:+int64', when='+int64')

    patch('0001-Fix-libdir-pkgconfig-variable.patch', when='@:6.1.1')
