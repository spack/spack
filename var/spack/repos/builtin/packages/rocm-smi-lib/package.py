# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import re
import shutil
import subprocess

from spack.package import *


class RocmSmiLib(CMakePackage):
    """It is a C library for Linux that provides a user space interface
    for applications to monitor and control GPU applications."""

    homepage = "https://github.com/ROCm/rocm_smi_lib"
    git = "https://github.com/ROCm/rocm_smi_lib.git"
    url = "https://github.com/ROCm/rocm_smi_lib/archive/rocm-6.0.2.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["librocm_smi64"]

    version("master", branch="master")
    version("6.0.2", sha256="61e755d710ff38425df3d262d1ad4c510d52d3c64e3fe15140c2575eba316949")
    version("6.0.0", sha256="0053b42402fd007e5ca9b3186c70f2c6f1b3026558f328722adadc2838c51309")
    version("5.7.1", sha256="4d79cb0482b2f801cc7824172743e3dd2b44b9f6784d1ca2e5067f2fbb4ef803")
    version("5.7.0", sha256="a399db3d9fc113ce2dd1ab5608a1cf9129ec4b6a2a79ab7922b1d9f43c454640")
    version("5.6.1", sha256="9e94f9a941202c3d7ce917fd1cd78c4e0f06f48d6c929f3aa916378ccef1e02c")
    version("5.6.0", sha256="88be875948a29454b8aacced8bb8ad967502a7a074ecbc579ed673c1650a2f7e")
    version("5.5.1", sha256="37f32350bfaf6c697312628696d1b1d5fd9165f183882759bc6cb9a5d65b9430")
    version("5.5.0", sha256="0703f49b1c2924cc1d3f613258eabdff1925cb5bcf7cf22bb6b955dd065e4ce8")
    version("5.4.3", sha256="34d550272e420684230ceb7845aefcef79b155e51cf9ec55e31fdba2a4ed177b")
    version("5.4.0", sha256="4b110c9ec104ec39fc458b1b6f693662ab75395b75ed402b671d8e58c7ae63fe")
    version("5.3.3", sha256="c2c2a377c2e84f0c40297a97b6060dddc49183c2771b833ebe91ed98a98e4119")
    version("5.3.0", sha256="8f72ad825a021d5199fb73726b4975f20682beb966e0ec31b53132bcd56c5408")
    with default_args(deprecated=True):
        version("5.2.3", sha256="fcf4f75a8daeca81ecb107989712c5f3776ee11e6eed870cb93efbf66ff1c384")
        version("5.2.1", sha256="07ad3be6f8c7d3f0a1b8b79950cd7839fb82972cef373dccffdbda32a3aca760")
        version("5.2.0", sha256="7bce567ff4e087598eace2cae72d24c98b2bcc93af917eafa61ec9d1e8ef4477")
        version("5.1.3", sha256="8a19ce60dc9221545aa50e83e88d8c4be9bf7cde2425cefb13710131dc1d7b1b")
        version("5.1.0", sha256="21b31b43015b77a9119cf4c1d4ff3864f9ef1f34e2a52a38f985a3f710dc5f87")
    version(
        "5.0.2",
        sha256="a169129e4ecd1cca134039dc1bf91e1b3721768781abfae4ae61fad60a633472",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="9d0e560072f815b441528a5d6124e901570a5a04e9cff1f21329861609b37203",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="d4a34db26852defb62817aa44f08ef96d678c63a6f33425bc9d48c18e5e37b7a",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="43a2cc2ec548cc28698ca4fa01a947a4414febd433936a8d9770bf6f6ed55e4f",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="ea2f9d8a9999e4aac1cb969e6bf2a9f0b6d02f29d0c319b36cce26412ab8a8b0",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="c3ff56a14d334cb688a2e9a748dac46d9c2f7f576fe1f53416b1a0edbe842f8b",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="c31bf91c492f00d0c5ab21e45afbd7baa990e4a8d7ce9b01e3b988e5fdd53f50",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="0c1d2152e40e14bb385071ae16e7573290fb9f74afa5ab887c54f4dd75849a6b",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="93d19229b5a511021bf836ddc2a9922e744bf8ee52ee0e2829645064301320f4",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="8bb2142640d1c6bf141f19accf809e61377a6e0c0222e47ac4daa5da2c85ddac",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="b2934b112542af56de2dc1d5bffff59957e21050db6e3e5abd4c99e46d4a0ffe",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="86250c9ae9dfb18d4f7259a5f2f09b21574d4996fe5034a739ce63a27acd0082",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="72d2a3deda0b55a2d92833cd648f50c7cb64f8341b254a0badac0152b26f1391",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="a5d2ec3570d018b60524f0e589c4917f03d26578443f94bde27a170c7bb21e6e",
        deprecated=True,
    )

    variant("shared", default=True, description="Build shared or static library")

    depends_on("cmake@3:", type="build")
    depends_on("python@3:", type=("build", "run"), when="@3.9.0:")

    for ver in ["5.5.0", "5.5.1", "5.6.0", "5.6.1", "5.7.0", "5.7.1", "6.0.0", "6.0.2"]:
        depends_on("rocm-core@" + ver, when="@" + ver)
    patch("disable_pdf_generation_with_doxygen_and_latex.patch", when="@4.5.2:5.6")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("CMAKE_INSTALL_LIBDIR", "lib"),
        ]
        return args

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            ver = "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        else:
            ver = None
        return ver

    @run_after("install")
    def post_install(self):
        if self.spec.satisfies("@:5.1"):
            shutil.rmtree(self.prefix.lib)
            install_tree(self.prefix.rocm_smi, self.prefix)
            shutil.rmtree(self.prefix.rocm_smi)
            os.remove(join_path(self.prefix.bin, "rsmiBindings.py"))
            symlink("../bindings/rsmiBindings.py", join_path(self.prefix.bin, "rsmiBindings.py"))

    test_src_dir = "tests/rocm_smi_test"

    @run_after("install")
    def cache_test_sources(self):
        """Copy the tests source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        if self.spec.satisfies("@:5.1.0"):
            return
        self.cache_extra_test_sources([self.test_src_dir])

    def test(self):
        if self.spec.satisfies("@:5.1.0"):
            print("Skipping: stand-alone tests")
            return
        exclude = "rsmitst.exclude"
        TOPOLOGY_SYSFS_DIR = "/sys/devices/virtual/kfd/kfd/topology/nodes"
        test_dir = join_path(self.test_suite.current_test_cache_dir, self.test_src_dir)
        with working_dir(test_dir, create=True):
            cmake_bin = join_path(self.spec["cmake"].prefix.bin, "cmake")
            prefixes = ";".join([self.spec["rocm-smi-lib"].prefix])
            cc_options = [
                "-DCMAKE_PREFIX_PATH=" + prefixes,
                "-DROCM_DIR=" + self.spec["rocm-smi-lib"].prefix,
                ".",
            ]
            self.run_test(cmake_bin, cc_options)
            make()

            # Since rsmitst internally attempts to run for every gpu the exclude test list will
            # be the union of all the excludes for all the devices on the system
            disabled_tests = ""
            if os.path.exists(TOPOLOGY_SYSFS_DIR):
                for file in os.listdir(TOPOLOGY_SYSFS_DIR):
                    name_file = os.path.join(TOPOLOGY_SYSFS_DIR, str(file), "name")
                    if os.path.exists(name_file):
                        with open(name_file, "r") as f:
                            node = f.readline().strip("\n")
                            if node:
                                cmd = "source " + exclude + ' && echo "${FILTER[' + node + ']}"'
                                node_tests = subprocess.check_output(
                                    cmd, shell=True, executable="/bin/bash"
                                )
                                node_tests = node_tests.decode("utf-8").strip("\n")
                                if node_tests:
                                    disabled_tests = disabled_tests + node_tests + ":"

            # disable tests under virtualization
            cmd = "source " + exclude + ' && echo "${FILTER[virtualization]}"'
            virtualization_tests = subprocess.check_output(cmd, shell=True, executable="/bin/bash")
            virtualization_tests = virtualization_tests.decode("utf-8").strip("\n")
            disabled_tests = disabled_tests + virtualization_tests

            # disable test that requires --privileged permissions
            privileged_tests = ":".join(
                [
                    "rsmitstReadWrite.TestPerfLevelReadWrite",
                    "rsmitstReadWrite.TestFrequenciesReadWrite",
                    "rsmitstReadWrite.TestPciReadWrite",
                    "rsmitstReadWrite.TestPerfCntrReadWrite",
                ]
            )
            disabled_tests = disabled_tests + ":" + privileged_tests

            self.run_test("rsmitst64", "--gtest_filter=-" + disabled_tests)
            make("clean")
