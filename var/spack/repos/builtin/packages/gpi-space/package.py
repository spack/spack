# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GpiSpace(CMakePackage):
    """
    GPI-Space is a task-based workflow management system for parallel
    applications. It allows the developers to build domain-specific workflows
    using their own parallelization patterns, data management policies and I/O
    routines, while relying on the runtime system for the workflow management.
    The GPI-Space ecosystem "auto-manages" the application with dynamic
    scheduling, built-in distributed memory transfers and distributed tasks
    execution.
    """

    homepage = "https://www.gpi-space.de"
    url      = "https://github.com/cc-hpc-itwm/gpispace/archive/refs/tags/v21.09.tar.gz"
    git      = "https://github.com/cc-hpc-itwm/gpispace.git"

    maintainers = ["mzeyen1985", "tiberot", "rumach", "mrahn", "acastanedam"]

    version("latest", branch="main")
    version('22.03', sha256='b01500b9480452aee865a0ef98cf40864f847b7e22ea572f9a6f0f5ac2ae9a1a')
    version('21.12.1', sha256='6c49aca95a32e66fa1e34bef542c2f380e91f86c9c2b3b0d98921901bab7abce')
    version('21.12',  sha256='51794e2b593b8d1dc7d6310e17744842919bf44205b2cb7a79de2f2bbac3352a')
    version('21.09',  sha256='7f3861c2bfec15a4da46378ea38b304e1462ed315cd315b81ab2c2a8ba50dd3e')

    variant("network",
            default="ethernet",
            values=("infiniband", "ethernet"),
            description="GPI-2 fabric to enable")
    variant("monitor",
            default=True,
            description="""
                        Enables the gspc-monitor application for execution monitoring.
                        """)
    variant("build_type",
            default="Release",
            values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
            description="CMake build type")

    depends_on("cmake@3.15.0:",
               type="build")
    depends_on("chrpath@0.13:",
               type=("build", "run"))
    depends_on("pkgconfig",
               type="build")
    depends_on("boost@1.62.0:1.63.0 +atomic +chrono +coroutine +context +date_time +filesystem +iostreams +program_options +random +regex +serialization +test +timer cxxstd=14")
    depends_on("hwloc@1.10: +libudev ~shared ~libxml2")
    depends_on("libssh2@1.7:")
    depends_on("openssl@0.9:")
    depends_on("gpi-2@1.3.2:1.3.3 fabrics=infiniband",
               when="network=infiniband")
    depends_on("gpi-2@1.3.2:1.3.3 fabrics=ethernet",
               when="network=ethernet")
    depends_on("qt@5.9:5.15",
               when="+monitor")

    def cmake_args(self):
        args = [self.define("FHG_ASSERT_MODE", False),
                self.define("INSTALL_DO_NOT_BUNDLE", True),
                self.define("BUILD_TESTING", False),
                self.define_from_variant("GSPC_WITH_MONITOR_APP", "monitor")]

        return args
