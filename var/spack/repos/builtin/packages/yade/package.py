from spack import *

class Yade(CMakePackage):
    """Yade is an free software for particle based simulations."""

    homepage = "https://gitlab.com/yade-dev/trunk"
    url = "https://gitlab.com/yade-dev/trunk/-/archive/2023.02a/trunk-2023.02a.tar.gz"

    version("2023.02a", sha256="f76b5a0aa7f202716efa94cd730e4bc442ffcb40a99caaf6e579ab8695efb0c1")

    def url_for_version(self, version):
        if version >= Version("2023.02a"):
            return super().url_for_version(version)
        url_fmt = "https://gitlab.com/yade-dev/trunk/-/archive/{0}/trunk-{0}.tar.gz"
        return url_fmt.format(version)

    def cmake_args(self):
        args = [
            self.define("CMAKE_INSTALL_PREFIX", self.prefix),
            self.define("BUILD_MJ2", False),
            self.define("BUILD_THIRDPARTY", False),
        ]
        return args