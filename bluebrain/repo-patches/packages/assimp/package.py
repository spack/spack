from spack import *
from spack.pkg.builtin.assimp import Assimp as BuiltinAssimp


class Assimp(BuiltinAssimp):
    version('4.1.0', sha256='3520b1e9793b93a2ca3b797199e16f40d61762617e072f2d525fad70f9678a71')
