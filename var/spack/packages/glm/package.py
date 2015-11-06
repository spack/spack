from spack import *


class Glm(Package):
    """
    OpenGL Mathematics (GLM) is a header only C++ mathematics library for graphics software based on
    the OpenGL Shading Language (GLSL) specification.
    """

    homepage = "https://github.com/g-truc/glm"
    url = "https://github.com/g-truc/glm/archive/0.9.7.1.tar.gz"

    version('0.9.7.1', '61af6639cdf652d1cdd7117190afced8')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            make("install")
