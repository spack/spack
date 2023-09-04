from spack.package import *


class Yade(CMakePackage):
    """Yade is an free software for particle based simulations."""

    homepage = "https://gitlab.com/yade-dev/trunk"
    url = "https://gitlab.com/yade-dev/trunk/-/archive/2023.02a/trunk-2023.02a.tar.gz"

    version("2023.02a", sha256="f76b5a0aa7f202716efa94cd730e4bc442ffcb40a99caaf6e579ab8695efb0c1")

    depends_on("cmake@3.0:", type="build")
    depends_on("gcc@4.2:", type=("build", "run"))
    depends_on("boost@1.47:", type=("build", "run"))
    depends_on("qt", type=("build", "run"))
    depends_on("freeglut", type=("build", "run"))
    depends_on("libqglviewer", type=("build", "run"))
    depends_on("python", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-ipython", type=("build", "run"))
    depends_on("py-sphinx", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("eigen@3.2.1:", type=("build", "run"))
    depends_on("gdb", type=("build", "run"))
    depends_on("sqlite", type=("build", "run"))

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
            self.define("CMAKE_BUILD_TYPE", "Release"),
        ]

        args.append("-DCMAKE_SOURCE_DIR={0}".format(self.stage.source_path))

        return args
