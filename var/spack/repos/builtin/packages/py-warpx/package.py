# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWarpx(PythonPackage):
    """This package is deprecated. Please use `warpx +python`.

    WarpX is an advanced electromagnetic Particle-In-Cell code. It supports
    many features including Perfectly-Matched Layers (PML) and mesh refinement.
    In addition, WarpX is a highly-parallel and highly-optimized code and
    features hybrid OpenMP/MPI parallelization, advanced vectorization
    techniques and load balancing capabilities.

    These are the Python bindings of WarpX with PICMI input support.
    See the C++ 'warpx' package for the WarpX application and library.
    """

    homepage = "https://ecp-warpx.github.io"
    url = "https://github.com/ECP-WarpX/WarpX/archive/refs/tags/23.08.tar.gz"
    git = "https://github.com/ECP-WarpX/WarpX.git"

    maintainers("ax3l", "dpgrote", "EZoni", "RemiLehe")

    tags = ["e4s", "ecp"]

    license("BSD-3-Clause-LBNL")

    # NOTE: if you update the versions here, also see warpx
    with default_args(deprecated=True):
        version("develop", branch="development")
        version("23.08", sha256="22b9ad39c89c3fae81b1ed49abd72f698fbc79d8ac3b8dd733fd02185c0fdf63")
        version("23.07", sha256="eab91672191d7bf521cda40f2deb71a144da452b35245567b14873938f97497e")
        version("23.06", sha256="9bbdcbfae3d7e87cd4457a0debd840897e9a9d15e14eaad4be8c8e16e13adca2")
        version("23.05", sha256="fa4f6d8d0537057313bb657c60d5fd91ae6219d3de95d446282f1ad47eeda863")
        version("23.04", sha256="90462a91106db8e241758aeb8aabdf3e217c9e3d2c531d6d30f0d03fd3ef789c")
        version("23.03", sha256="26e79f8c7f0480b5f795d87ec2663e553b357894fc4b591c8e70d64bfbcb72a4")
        version("23.02", sha256="596189e5cebb06e8e58a587423566db536f4ac3691d01db8d11f5503f1e7e35e")
        version("23.01", sha256="ed0536ae5a75df4b93c275c6839a210fba61c9524a50ec6217c44d5ac83776b3")
        version("22.12", sha256="bdd0a9ec909a5ac00f288bb4ab5193136b460e39e570ecb37d3d5d742b7e67bf")
        version("22.11", sha256="03c580bcd0cf7b99a81b9ef09d14172c96672c7fb028a0ed6728b3cc9ec207e7")
        version("22.10", sha256="736747184eaae65fb1bbeb6867b890c90b233132bc185d85ea605525637e7c53")
        version("22.09", sha256="0dc7076bad1c46045abd812729fa650bc4f3d17fdfded6666cbaf06da70f09d7")
        version("22.08", sha256="95930c4f4fc239dfe4ed36b1023dd3768637ad37ff746bb33cf05231ca08ee7a")
        version("22.07", sha256="7d91305f8b54b36acf2359daec5a94e154e2a8d7cbae97429ed8e93f7c5ea661")
        version("22.06", sha256="faa6550d7dd48fc64d4b4d67f583d34209c020bf4f026d10feb7c9b224caa208")
        version("22.05", sha256="be97d695a425cfb0ecd3689a0b9706575b7b48ce1c73c39d4ea3abd616b15ad7")
        version("22.04", sha256="ff6e3a379fafb76e311b2f48089da6b1ab328c5b52eccd347c41cce59d0441ed")
        version("22.03", sha256="808a9f43514ee40fa4fa9ab5bf0ed11219ab6f9320eb414bb4f043fab112f7a0")
        version("22.02", sha256="3179c54481c5dabde77a4e9a670bb97b599cecc617ad30f32ab3177559f67ffe")
        version("22.01", sha256="73a65c1465eca80f0db2dab4347c22ddf68ad196e3bd0ccc0861d782f13b7388")

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI support")

    for v in [
        "23.08",
        "23.07",
        "23.06",
        "23.05",
        "23.04",
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
        "develop",
    ]:
        depends_on("warpx@{0}".format(v), when="@{0}".format(v), type=["build", "link"])

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("python@3.8:", type=("build", "run"), when="@23.09:")
    depends_on("py-numpy@1.15.0:1", type=("build", "run"))
    depends_on("py-mpi4py@2.1.0:", type=("build", "run"), when="+mpi")
    depends_on("py-periodictable@1.5:1", type=("build", "run"))
    depends_on("py-picmistandard@0.25.0", type=("build", "run"), when="@23.07:")
    depends_on("py-picmistandard@0.24.0", type=("build", "run"), when="@23.06")
    depends_on("py-picmistandard@0.23.2", type=("build", "run"), when="@23.04:23.05")
    depends_on("py-picmistandard@0.0.22", type=("build", "run"), when="@22.12:23.03")
    depends_on("py-picmistandard@0.0.20", type=("build", "run"), when="@22.10:22.11")
    depends_on("py-picmistandard@0.0.19", type=("build", "run"), when="@22.02:22.09")
    depends_on("py-picmistandard@0.0.18", type=("build", "run"), when="@22.01")
    depends_on("py-setuptools@42:", type="build")
    # Since we use PYWARPX_LIB_DIR to pull binaries out of the
    # 'warpx' spack package, we don't need cmake as declared
    depends_on("warpx +lib ~mpi +shared", type=("build", "link"), when="~mpi")
    depends_on("warpx +lib +mpi +shared", type=("build", "link"), when="+mpi")

    def setup_build_environment(self, env):
        env.set("PYWARPX_LIB_DIR", self.spec["warpx"].prefix.lib)
