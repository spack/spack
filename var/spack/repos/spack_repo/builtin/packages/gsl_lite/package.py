# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class GslLite(CMakePackage):
    """ISO C++ Core Guidelines Library implementation for C++98, C++11 up"""

    homepage = "https://github.com/gsl-lite/gsl-lite"
    git = "https://github.com/gsl-lite/gsl-lite.git"
    url = "https://github.com/gsl-lite/gsl-lite/archive/refs/tags/v0.38.1.tar.gz"

    maintainers("AlexanderRichert-NOAA", "climbfuji", "edwardhartnett", "Hang-Lei-NOAA")

    license("MIT")

    version("1.0.1", sha256="063a0b4248a2afd8154b2b5fe9d64472868a166d3963682e823f81516194af79")
    version("0.43.0", sha256="e48c3138648156d2b85905b1d280d661fad61524c5c0ca10d3857036ca3dd519")
    version("0.42.0", sha256="54a1b6f9db72eab5d8dcaf06b36d32d4f5da3471d91dac71aba19fe15291a773")
    version("0.41.0", sha256="4682d8a60260321b92555760be3b9caab60e2a71f95eddbdfb91e557ee93302a")
    version("0.40.0", sha256="65af4ec8a1050dac4f1ca4622881bb02a9c3978a9baec289fb56e25412d6cac7")
    version("0.39.0", sha256="f80ec07d9f4946097a1e2554e19cee4b55b70b45d59e03a7d2b7f80d71e467e9")
    version("0.38.1", sha256="c2fa2315fff312f3897958903ed4d4e027f73fa44235459ecb467ad7b7d62b18")
    version("0.38.0", sha256="5d25fcd31ea66dac9e14da1cad501d95450ccfcb2768fffcd1a4170258fcbc81")
    version("0.37.0", sha256="a31d51b73742bb234acab8d2411223cf299e760ed713f0840ffed0dabe57ca38")
    version("0.36.0", sha256="c052cc4547b33cedee6f000393a7005915c45c6c06b35518d203db117f75c71c")
    version("0.34.0", sha256="a7d5b2672b78704ca03df9ef65bc274d8f8cacad3ca950365eef9e25b50324c5")

    depends_on("cxx", type="build")  # generated
