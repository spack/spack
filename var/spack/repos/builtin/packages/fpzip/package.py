from spack.package import *


class Fpzip(CMakePackage):
    """fpzip compressor"""

    homepage = "https://github.com/llnl/fpzip"
    url = "https://github.com/LLNL/fpzip/releases/download/1.3.0/fpzip-1.3.0.tar.gz"
    git = "https://github.com/llnl/fpzip"

    version("master", branch="master")
    version("1.3.0", sha256="248df7d84259e3feaa4c4797956b2a77c3fcd734e8f8fdc51ce171dcf4f0136c")
