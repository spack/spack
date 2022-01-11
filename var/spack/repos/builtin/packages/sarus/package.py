# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

from spack import *


class Sarus(CMakePackage):
    """Sarus is an OCI-compliant container engine for HPC systems."""

    homepage = "https://github.com/eth-cscs/sarus"
    url = "https://github.com/eth-cscs/sarus/archive/1.3.3.tar.gz"
    git = "https://github.com/eth-cscs/sarus.git"
    maintainers = ["Madeeks", "teonnik"]

    version("develop", branch="develop")
    version("master", branch="master")
    version(
        "1.4.0",
        sha256="59cdb957bcf34b5f85999165986c0b45e9694facfb851f6504ec1fa1c7d77221",
    )
    version(
        "1.3.3",
        sha256="792741601ef4b8aa60f55a698f7e08fd510786f636d42285ddcbe659a914fe66",
    )
    version(
        "1.3.2",
        sha256="94d571c3eab7df195c17387818c6f652a6b2301a4e56081aaea74d4d19a4bd07",
    )
    version(
        "1.3.1",
        sha256="7809f4ecf6d65cd5791b74cd296da407d68a2e6fbc319e1af9c0d33c2830d979",
    )
    version(
        "1.3.0",
        sha256="3f11b3bd58c44d165762bff5e53b081e729486df98f4fe6fecde104e21eab131",
    )
    version(
        "1.2.0",
        sha256="c5eca12e4cf96ab586401546d932afb33952d60b10048ff7382526a7ac8fe591",
    )
    version(
        "1.1.0",
        sha256="79f3d3e0eef94c42a0356a012291afb42d79cc09f5d92dc241d9a8c743cfae83",
    )
    version(
        "1.0.1",
        sha256="6422805a496a738f43f137291761ca21c1e46303b2eea0777f36d3dbcbc622fa",
    )
    version(
        "1.0.0",
        sha256="b08f26b8249a064d6a45d935b96efc04e25070a03ac8002d0e427da0598d51fc",
    )

    variant(
        "ssh",
        default=False,
        description="Build and install the SSH hook and custom SSH software "
        "to enable connections inside containers",
    )

    depends_on("expat", type="build")
    depends_on("squashfs", type=("build", "run"))
    depends_on("boost@1.65.0: cxxstd=11")
    depends_on("cpprestsdk@2.10.0:")
    depends_on("libarchive@3.4.1:")
    depends_on("rapidjson@1.2.0-2021-08-13", type="build")
    depends_on("runc")
    depends_on("tini")

    # autoconf is required to build Dropbear for the SSH hook
    depends_on("autoconf", type="build")

    # Python 3 is used to run integration tests
    depends_on("python@3:", type="test", when="@develop")

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DCMAKE_TOOLCHAIN_FILE=./cmake/toolchain_files/gcc.cmake",
            "-DENABLE_SSH=%s" % ("+ssh" in spec),
        ]
        return args

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make(*self.install_targets)
            mkdirp(prefix.var.OCIBundleDir)

    @run_after("install")
    def build_perms_script(self):
        script_sh = join_path(self.spec.prefix, "configure_installation.sh")
        tty.warn(
            """
                To complete Sarus's configuration:

                1. Make sure sarus and its dependencies (tini, squashfs) are in PATH, for example do `spack load sarus`.
                2. Execute the script {} with root privileges.

                The script generates a basic working configuration. For more details:

                https://sarus.readthedocs.io/en/stable/config/basic_configuration.html
            """.format(
                script_sh
            )
        )
