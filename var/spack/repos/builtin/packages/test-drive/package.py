from spack.package import *


class TestDrive(MesonPackage):
    """Simple testing framework for Fortran packages"""

    homepage = "https://github.com/fortran-lang/test-drive"
    url = "https://github.com/fortran-lang/test-drive/releases/download/v0.4.0/test-drive-0.4.0.tar.xz"

    maintainers("awvwgk")

    version("0.4.0", "effabe5d46ea937a79f3ea8d37eea43caf38f9f1377398bad0ca02784235e54a")