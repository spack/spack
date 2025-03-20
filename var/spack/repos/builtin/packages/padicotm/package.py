# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.puk import Puk


class Padicotm(AutotoolsPackage):
    """PadicoTM communication framework and launcher.

    PadicoTM is the runtime infrastructure for the Padico software
    environment for computational grids. It is composed of a core
    which provides a high-performance framework for networking and
    multi-threading, on top of which the abstraction layer is built
    with freely and dynamically assembled components. Various
    communications methods are embedded in components that the user
    may assemble to get the needed communication stack.
    """

    homepage = "https://pm2.gitlabpages.inria.fr/PadicoTM/"
    url = "https://pm2.gitlabpages.inria.fr/releases/"
    list_url = "https://pm2.gitlabpages.inria.fr/releases/"
    git = "https://gitlab.inria.fr/pm2/pm2.git"

    maintainers("a-denis")
    license("GPL-2.0-or-later", checked_by="a-denis")

    def url_for_version(self, version):
        url = "https://pm2.gitlabpages.inria.fr/releases/pm2-{0}.tar.gz"
        return url.format(version)

    version("master", branch="master")
    version(
        "2025-03-18", sha256="2d0208809dd17bac4fd7e7f97b22e2240b925d8828b9ab5dc5f435e58ff97010"
    )
    version(
        "2024-11-21", sha256="76da169bbb9720a13be1f750480e1a7d6510830163878852876932639879d632"
    )
    version(
        "2024-07-12", sha256="ea9bb91b213950a52eb99d787110905d45ed02954ea9133596d690db5be0c31b"
    )
    version(
        "2022-05-31", sha256="afd19809a5a520a477ab596f951bbde3209868ab16febbc246592e8aed20c3ca"
    )
    version(
        "2021-05-21", sha256="6a207b032e623b8be0196a42dcaf4311bfe45ede2e044bd47611b6610c04c61e"
    )

    variant("optimize", default=True, description="Build in optimized mode")
    variant("debug", default=False, description="Build in debug mode")
    variant("asan", default=False, description="Build with Address Sanitizer (ASAN)")
    variant("pukabi", default=False, description="Build with PukABI")
    variant("pioman", default=True, description="use pioman I/O manager")
    variant("ibverbs", default=True, description="use InfiniBand ibverbs")
    variant("psm", default=False, description="use Intel Performance Scaled Messaging (PSM)")
    variant("psm2", default=False, description="use Intel Performance Scaled Messaging 2 (PSM2)")
    variant("ofi", default=True, description="use OpenFabric Interface (libfabric)")
    variant("craypmi", default=False, description="use Cray PMI support")
    variant("pmix", default=True, description="use slurm PMIx support")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("autoconf@2.69:", type="build")
    depends_on("gmake", type="build")

    depends_on("hwloc@2.0.0:", type=("build", "link", "run"))
    depends_on("zlib")
    depends_on("lz4")
    depends_on("rdma-core", when="+ibverbs")
    depends_on("psm", when="+psm")
    depends_on("opa-psm2", when="+psm2")
    depends_on("libfabric", when="+ofi")
    depends_on("cray-pmi", when="+craypmi")
    depends_on("pmix", when="+pmix")
    requires("+pukabi", when="+ibverbs", msg="ibverbs rcache requires pukabi")

    for v in Puk.versions:
        depends_on(f"puk@{v}", when=f"@{v}")
        depends_on(f"pukabi@{v}", when=f"@{v} +pukabi")
        depends_on(f"pioman@{v}", when=f"@{v} +pioman")

    depends_on("puk")
    depends_on("pukabi", when="+pukabi")
    depends_on("pioman", when="+pioman")
    depends_on("puk+asan", when="+asan")

    conflicts("+pukabi", when="+asan", msg="PukABI and ASAN conflicts for LD_PRELOAD")
    conflicts("platform=darwin", msg="Darwin is not supported.")
    conflicts("platform=windows", msg="Windows is not supported.")
    conflicts("%gcc@:5", msg="Requires at least gcc 6.")
    conflicts("%gcc@14:", when="@:2024-07-12", msg="Older release do not support gcc >= 14")

    configure_directory = "PadicoTM"
    build_directory = "build"

    def autoreconf(self, spec, prefix):
        with working_dir(self.configure_directory):
            Executable("./autogen.sh")()

    def configure_args(self):
        config_args = ["--without-portals4"]  # portals4 not packaged in spack
        config_args += self.enable_or_disable("optimize")
        config_args += self.enable_or_disable("debug")
        config_args += self.enable_or_disable("asan")
        config_args += self.with_or_without("pukabi")
        config_args += self.with_or_without("pioman")
        config_args += self.with_or_without("psm")
        config_args += self.with_or_without("psm2")
        config_args += self.with_or_without("ofi")
        config_args += self.with_or_without("ibverbs")
        config_args += self.with_or_without("pmix")
        config_args += self.with_or_without("pmi2", variant="craypmi")
        return config_args
