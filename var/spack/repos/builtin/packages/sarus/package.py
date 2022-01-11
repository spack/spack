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
    version("1.4.0", tag="1.4.0")
    version("1.3.3", tag="1.3.3")
    version("1.3.2", tag="1.3.2")
    version("1.3.1", tag="1.3.1")
    version("1.3.0", tag="1.3.0")
    version("1.2.0", tag="1.2.0")
    version("1.1.0", tag="1.1.0")
    version("1.0.1", tag="1.0.1")
    version("1.0.0", tag="1.0.0")

    variant(
        "ssh",
        default=False,
        description="Build and install the SSH hook and custom SSH software "
        "to enable connections inside containers",
    )

    depends_on("wget", type="build")
    depends_on("expat", type="build")
    depends_on("squashfs", type=("build", "run"))
    depends_on("boost@1.65.0: cxxstd=11")
    depends_on("cpprestsdk@2.10.0:")
    depends_on("libarchive@3.4.1:")
    depends_on("rapidjson@00dbcf2", type="build")
    depends_on("runc")
    depends_on("tini")

    # autoconf is required to build Dropbear for the SSH hook
    depends_on("autoconf", type="build")

    # Python 3 is used to run integration tests
    depends_on("python@3:", type="run", when="@develop")

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

                1. Make sure `tini`, `tini-static` and `squashfs` binaries are in PATH, for example do `spack load tini squashfs`.
                2. Execute the script {} with root privileges.

                The script generates a basic working configuration. For more details:

                https://sarus.readthedocs.io/en/stable/config/basic_configuration.html
            """.format(
                script_sh
            )
        )
