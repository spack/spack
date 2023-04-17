# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWarpx(PythonPackage):
    """WarpX is an advanced electromagnetic Particle-In-Cell code. It supports
    many features including Perfectly-Matched Layers (PML) and mesh refinement.
    In addition, WarpX is a highly-parallel and highly-optimized code and
    features hybrid OpenMP/MPI parallelization, advanced vectorization
    techniques and load balancing capabilities.

    These are the Python bindings of WarpX with PICMI input support.
    See the C++ 'warpx' package for the WarpX application and library.
    """

    homepage = "https://ecp-warpx.github.io"
    url = "https://github.com/ECP-WarpX/WarpX/archive/refs/tags/23.03.tar.gz"
    git = "https://github.com/ECP-WarpX/WarpX.git"

    maintainers("ax3l", "dpgrote", "RemiLehe")

    tags = ["e4s", "ecp"]

    # NOTE: if you update the versions here, also see warpx
    version("develop", branch="development")
    version("23.03", sha256="e1274aaa2a2c83d599d61c6e4c426db4ed5d4c5dc61a2002715783a6c4843718")
    version("23.02", sha256="a6c63ebc38cbd224422259a814be501ac79a3b734dab7f59500b6957cddaaac1")
    version("23.01", sha256="e853d01c20ea00c8ddedfa82a31a11d9d91a7f418d37d7f064cf8a241ea4da0c")
    version("22.12", sha256="96019902cd6ea444a1ae515e8853048e9074822c168021e4ec1687adc72ef062")
    version("22.11", sha256="528f65958f2f9e60a094e54eede698e871ccefc89fa103fe2a6f22e4a059515e")
    version("22.10", sha256="3cbbbbb4d79f806b15e81c3d0e4a4401d1d03d925154682a3060efebd3b6ca3e")
    version("22.09", sha256="dbef1318248c86c860cc47f7e18bbb0397818e3acdfb459e48075004bdaedea3")
    version("22.08", sha256="5ff7fd628e8bf615c1107e6c51bc55926f3ef2a076985444b889d292fecf56d4")
    version("22.07", sha256="0286adc788136cb78033cb1678d38d36e42265bcfd3d0c361a9bcc2cfcdf241b")
    version("22.06", sha256="e78398e215d3fc6bc5984f5d1c2ddeac290dcbc8a8e9d196e828ef6299187db9")
    version("22.05", sha256="2fa69e6a4db36459b67bf663e8fbf56191f6c8c25dc76301dbd02a36f9b50479")
    version("22.04", sha256="9234d12e28b323cb250d3d2cefee0b36246bd8a1d1eb48e386f41977251c028f")
    version("22.03", sha256="ddbef760c8000f2f827dfb097ca3359e7aecbea8766bec5c3a91ee28d3641564")
    version("22.02", sha256="d74b593d6f396e037970c5fbe10c2e5d71d557a99c97d40e4255226bc6c26e42")
    version("22.01", sha256="e465ffadabb7dc360c63c4d3862dc08082b5b0e77923d3fb05570408748b0d28")
    version("21.12", sha256="847c98aac20c73d94c823378803c82be9a14139f1c14ea483757229b452ce4c1")
    version("21.11", sha256="ce60377771c732033a77351cd3500b24b5d14b54a5adc7a622767b9251c10d0b")
    version("21.10", sha256="d372c573f0360094d5982d64eceeb0149d6620eb75e8fdbfdc6777f3328fb454")
    version("21.09", sha256="861a65f11846541c803564db133c8678b9e8779e69902ef1637b21399d257eab")
    version("21.08", sha256="6128a32cfd075bc63d08eebea6d4f62d33ce0570f4fd72330a71023ceacccc86")
    version("21.07", sha256="a8740316d813c365715f7471201499905798b50bd94950d33f1bd91478d49561")
    version("21.06", sha256="a26039dc4061da45e779dd5002467c67a533fc08d30841e01e7abb3a890fbe30")
    version("21.05", sha256="f835f0ae6c5702550d23191aa0bb0722f981abb1460410e3d8952bc3d945a9fc")
    version("21.04", sha256="51d2d8b4542eada96216e8b128c0545c4b7527addc2038efebe586c32c4020a0")

    variant("mpi", default=True, description="Enable MPI support")

    for v in [
        "23.03",
        "23.02",
        "23.01",
        "22.12",
        "22.11",
        "22.10",
        "22.09",
        "22.08",
        "22.07",
        "22.06",
        "22.05",
        "22.04",
        "22.03",
        "22.02",
        "22.01",
        "21.12",
        "21.11",
        "21.10",
        "21.09",
        "21.08",
        "21.07",
        "21.06",
        "21.05",
        "21.04",
        "develop",
    ]:
        depends_on("warpx@{0}".format(v), when="@{0}".format(v), type=["build", "link"])

    depends_on("python@3.6:3.9", type=("build", "run"), when="@:21.12")
    depends_on("python@3.6:", type=("build", "run"), when="@22.01:")
    depends_on("py-numpy@1.15.0:1", type=("build", "run"))
    depends_on("py-mpi4py@2.1.0:", type=("build", "run"), when="+mpi")
    depends_on("py-periodictable@1.5:1", type=("build", "run"))
    depends_on("py-picmistandard@0.0.14", type=("build", "run"), when="@21.03:21.11")
    depends_on("py-picmistandard@0.0.16", type=("build", "run"), when="@21.12")
    depends_on("py-picmistandard@0.0.18", type=("build", "run"), when="@22.01")
    depends_on("py-picmistandard@0.0.19", type=("build", "run"), when="@22.02:22.09")
    depends_on("py-picmistandard@0.0.20", type=("build", "run"), when="@22.10:22.11")
    depends_on("py-picmistandard@0.0.22", type=("build", "run"), when="@22.12:")
    depends_on("py-setuptools@42:", type="build")
    # Since we use PYWARPX_LIB_DIR to pull binaries out of the
    # 'warpx' spack package, we don't need py-cmake as declared
    # depends_on('py-cmake@3.15:3', type='build')
    # depends_on('py-cmake@3.18:3', type='build', when='@22.01:')
    depends_on("py-wheel", type="build")
    depends_on("warpx +lib ~mpi +shared", type=("build", "link"), when="~mpi")
    depends_on("warpx +lib +mpi +shared", type=("build", "link"), when="+mpi")

    def setup_build_environment(self, env):
        env.set("PYWARPX_LIB_DIR", self.spec["warpx"].prefix.lib)
