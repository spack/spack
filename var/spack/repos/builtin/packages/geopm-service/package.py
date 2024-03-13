# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class GeopmService(AutotoolsPackage):
    """The Global Extensible Open Power Manager (GEOPM) is a framework for
    exploring power and energy optimizations targeting heterogeneous platforms.
    The GEOPM package provides many built-in features. A simple use case is
    reading hardware counters and setting hardware controls with platform
    independent syntax using a command line tool on a particular compute node.
    An advanced use case is dynamically coordinating hardware settings across
    all compute nodes used by a distributed application is response to the
    application's behavior and requests from the resource manager.

    Note: GEOPM interfaces with hardware using Model Specific Registers (MSRs).
    For proper usage make sure MSRs are made available via the msr or
    msr-safe kernel modules by your administrator."""

    homepage = "https://geopm.github.io"
    git = "https://github.com/geopm/geopm.git"
    url = "https://github.com/geopm/geopm/tarball/v3.0.1"

    maintainers("bgeltz", "cmcantalupo")
    license("BSD-3-Clause")
    tags = ["e4s"]

    version("develop", branch="dev", get_full_repo=True)
    version("3.0.1", sha256="32ba1948de58815ee055470dcdea64593d1113a6cad70ce00ab0286c127f8234")

    variant("debug", default=False, description="Enable debug")
    variant("docs", default=True, description="Create man pages with Sphinx")
    variant(
        "systemd",
        default=False,
        description="Enable use of systemd (systemd development libraries required)",
    )
    variant("liburing", default=True, description="Enables the use of liburing for batch I/O")
    variant(
        "libcap", default=True, description="Enables the use of libcap to do capabilities checks"
    )
    variant("gnu-ld", default=False, description="Assume C compiler uses gnu-ld")

    variant("levelzero", default=False, description="Enables the use of oneAPI Level Zero loader")
    variant("nvml", default=False, description="Enable NVML support")

    variant(
        "rawmsr",
        default=True,
        description="Enable direct use of standard msr device driver",
        when="@develop",
    )

    conflicts("+nvml", when="+levelzero", msg="LevelZero and NVML support are mutually exclusive")

    conflicts("%gcc@:7.2", msg="Requires C++17 support")
    conflicts("%clang@:4", msg="Requires C++17 support")

    conflicts("platform=darwin", msg="Darwin is not supported")
    conflicts("platform=windows", msg="Windows is not supported")

    conflicts("target=aarch64:", msg="Only available on x86_64")
    conflicts("target=ppc64:", msg="Only available on x86_64")
    conflicts("target=ppc64le:", msg="Only available on x86_64")

    patch("0001-Support-NVML-via-CUDA-installation.patch", when="+nvml")

    # Autotools dependencies
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("file")

    # Docs dependencies
    depends_on("doxygen", type="build", when="+docs")
    depends_on("py-docstring-parser@0.13.0:", type="build", when="+docs")
    depends_on("py-sphinx@4.5:", type="build", when="+docs")
    depends_on("py-sphinx-rtd-theme@1:", type="build", when="+docs")
    depends_on("py-sphinxemoji@0.2.0:", type="build", when="+docs")
    depends_on("py-sphinx-tabs@3.3.1:", type="build", when="+docs")
    depends_on("py-pygments@2.13.0:", type="build", when="+docs")

    # Other Python dependencies - from service/setup.py
    depends_on("py-dasbus@1.6.0:", type=("build", "run"))
    depends_on("py-cffi@1.14.5:", type="run")
    depends_on("py-psutil@5.8.0:", type="run")
    depends_on("py-jsonschema@3.2.0:", type="run")
    depends_on("py-pyyaml@6.0:", type="run")
    depends_on("py-setuptools@53.0.0:", type="build")

    # Other dependencies
    depends_on("bash-completion")
    depends_on("unzip")
    depends_on("libcap", when="+libcap")
    depends_on("liburing", when="+liburing")
    depends_on("oneapi-level-zero", when="+levelzero")
    depends_on("cuda", when="+nvml")

    extends("python")

    configure_directory = "service"

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        with working_dir("service"):
            if not spec.version.isdevelop():
                # Required to workaround missing VERSION files
                # from GitHub generated source tarballs
                with open("VERSION_OVERRIDE", "w") as fd:
                    fd.write(f"{spec.version}")
            bash("./autogen.sh")

    def configure_args(self):
        args = [
            "--with-bash-completion-dir="
            + join_path(self.spec.prefix, "share", "bash-completion", "completions")
        ]

        args += self.enable_or_disable("debug")
        args += self.enable_or_disable("docs")
        args += self.enable_or_disable("systemd")
        args += self.enable_or_disable("liburing")
        args += self.with_or_without("liburing", activation_value="prefix")
        args += self.enable_or_disable("libcap")
        args += self.with_or_without("gnu-ld")

        args += self.enable_or_disable("levelzero")
        args += self.enable_or_disable("nvml")
        if "+nvml" in self.spec:
            args += [
                "--with-nvml=" + join_path(self.spec["cuda"].prefix, "targets", "x86_64-linux")
            ]

        args += self.enable_or_disable("rawmsr")
        return args

    def setup_run_environment(self, env):
        # Required to ensure geopmdpy can load
        # libgeopmd.so.2 via CFFI
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib
        env.prepend_path("LD_LIBRARY_PATH", lib_dir)
