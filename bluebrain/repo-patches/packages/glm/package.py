from spack import *
from spack.pkg.builtin.glm import Glm as BuiltinGlm


class Glm(BuiltinGlm):
    version('0.9.9.3', sha256='fba9fd177073a36c5a7798c74b28e79ba6deb8f4bb0d2dbfc0e207c27da7e12c')
