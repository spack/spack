# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class GeopmRuntime(AutotoolsPackage):
    """The Global Extensible Open Power Manager (GEOPM) Runtime is designed to
    enhance energy efficiency of applications through active hardware
    configuration."""

    homepage = "https://geopm.github.io"
    git = "https://github.com/geopm/geopm.git"
    url = "https://github.com/geopm/geopm/tarball/v3.0.1"

    maintainers("bgeltz", "cmcantalupo")
    license("BSD-3-Clause")
    tags = ["e4s"]

    version("develop", branch="dev", get_full_repo=True)
    version("3.0.1", sha256="32ba1948de58815ee055470dcdea64593d1113a6cad70ce00ab0286c127f8234")

    variant("debug", default=False, description="Enable debug")
    variant("docs", default=False, description="Create man pages with Sphinx")
    variant("overhead", default=False, description="Track time spent in GEOPM API calls")
    variant("beta", default=False, description="Enable beta features")
    variant("mpi", default=True, description="Enable MPI dependent components")
    variant("fortran", default=True, description="Build fortran interface")
    variant("openmp", default=True, description="Build with OpenMP")
    variant("ompt", default=True, description="Use OpenMP Tools Interface")
    variant("gnu-ld", default=False, description="Assume C compiler uses gnu-ld")
    variant("intel-mkl", default=True, description="Build with Intel MKL support")
    variant(
        "checkprogs",
        default=False,
        description='Build tests (use with "devbuild" or "install --keep-stage")',
    )

    conflicts("%gcc@:7.2", msg="Requires C++17 support")
    conflicts("%clang@:4", msg="Requires C++17 support")
    conflicts("%gcc", when="+ompt")

    conflicts("platform=darwin", msg="Darwin is not supported")
    conflicts("platform=windows", msg="Windows is not supported")

    conflicts("target=aarch64:", msg="Only available on x86_64", when="@3.0.1")
    conflicts("target=ppc64:", msg="Only available on x86_64", when="@3.0.1")
    conflicts("target=ppc64le:", msg="Only available on x86_64", when="@3.0.1")

    # Autotools dependencies
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("file")

    # Docs dependencies
    depends_on("doxygen", type="build", when="+docs")
    depends_on("py-sphinx", type="build", when="+docs")
    depends_on("py-sphinx-rtd-theme@1:", type="build", when="+docs")
    depends_on("py-sphinxemoji@0.2.0:", type="build", when="+docs")
    depends_on("py-sphinx-tabs@3.3.1:", type="build", when="+docs")
    depends_on("py-pygments@2.13.0:", type="build", when="+docs")

    # Other Python dependencies - from scripts/setup.py
    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-setuptools@53.0.0:", type="build")
    depends_on("py-cffi@1.14.5:", type="run")
    depends_on("py-natsort@8.2.0:", type="run")
    depends_on("py-numpy@1.19.5:", type="run")
    depends_on("py-pandas@1.1.5:", type="run")
    depends_on("py-tables@3.7.0:", type="run")
    depends_on("py-psutil@5.8.0:", type="run")
    depends_on("py-pyyaml@6.0:", type="run")
    depends_on("py-docutils@0.18:", type="run", when="+checkprogs")

    # Other dependencies
    for ver in ["3.0.1", "develop"]:
        depends_on(f"geopm-service@{ver}", type="build", when=f"@{ver}")
        depends_on(f"py-geopmdpy@{ver}", type="run", when=f"@{ver}")
    depends_on("bash-completion")
    depends_on("unzip")
    depends_on("mpi@2.2:", when="+mpi")
    depends_on("libelf")
    depends_on("numactl", type="run", when="+checkprogs")
    depends_on("stress-ng", type="run", when="+checkprogs")

    # Intel dependencies
    depends_on("intel-oneapi-mkl%oneapi", when="+intel-mkl")

    extends("python")

    @property
    def install_targets(self):
        target = ["install"]
        if "+checkprogs" in self.spec:
            target += ["checkprogs"]
        return target

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        if not spec.version.isdevelop():
            # Required to workaround missing VERSION files
            # from GitHub generated source tarballs
            with open("VERSION_OVERRIDE", "w") as fd:
                fd.write(f"{spec.version}")
        bash("./autogen.sh")

    def configure_args(self):
        args = [
            "--with-bash-completion-dir="
            + join_path(self.spec.prefix, "share", "bash-completion", "completions"),
            "--disable-geopmd-local",
            f"--with-geopmd={self.spec['geopm-service'].prefix}",
        ]

        args += self.enable_or_disable("debug")
        args += self.enable_or_disable("docs")
        args += self.enable_or_disable("overhead")
        args += self.enable_or_disable("beta")
        args += self.enable_or_disable("mpi")
        args += self.enable_or_disable("fortran")
        args += self.enable_or_disable("openmp")
        args += self.enable_or_disable("ompt")
        args += self.with_or_without("gnu-ld")

        return args

    def setup_run_environment(self, env):
        # Required to ensure libgeopm.so
        # can be used with LD_PRELOAD
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib
        env.prepend_path("LD_LIBRARY_PATH", lib_dir)

        if "+checkprogs" in self.spec:
            env.set("GEOPM_SOURCE", self.stage.source_path)
            env.prepend_path("PYTHONPATH", self.stage.source_path)
        env.set("GEOPM_INSTALL", self.prefix)
