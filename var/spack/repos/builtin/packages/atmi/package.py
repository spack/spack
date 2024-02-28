# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Atmi(CMakePackage):
    """Asynchronous Task and Memory Interface, or ATMI, is a runtime framework
    and programming model for heterogeneous CPU-GPU systems. It provides a
    consistent, declarative API to create task graphs on CPUs and GPUs
    (integrated and discrete)."""

    homepage = "https://github.com/ROCm/atmi"
    git = "https://github.com/ROCm/atmi.git"
    url = "https://github.com/ROCm/atmi/archive/rocm-6.0.0.tar.gz"
    tags = ["rocm"]

    license("MIT")

    maintainers("srekolam", "renjithravindrankannath")
    version("5.5.1", sha256="6b3ee68433506315b55d093a4b47463916874fb6f3f602098eaff2ec283e69ab")
    version("5.5.0", sha256="b8bfd32e5c386f5169da62172964343f9b7fad207e0e74dd1093c7acf06d9811")
    version("5.4.3", sha256="243aae6614e5bd136a099102957a6d65a01434b620291349613ad63701868ef8")
    version("5.4.0", sha256="b5cce10d7099fecbb40a0d9c2f29a7675315471fe145212b375e37e4c8ba5618")
    version("5.3.3", sha256="cc1144e4939cea2944f6c72a21406b9dc5b56d933696494074c280df7469834a")
    version("5.3.0", sha256="dffc0eb0bc1617843e7f728dbd6c8b12326c5c8baa34369aa267aab40f5deb6a")
    with default_args(deprecated=True):
        version("5.2.3", sha256="5f66c59e668cf968e86b556a0a52ee0202d1b370d8406e291a874cbfd200ee17")
        version("5.2.1", sha256="6b33445aa67444c038cd756f855a58a72dd35db57e7b63da37fe78a8585b982b")
        version("5.2.0", sha256="33e77905a607734157d46c736c924c7c50b6b13f2b2ddbf711cb08e37f2efa4f")
        version("5.1.3", sha256="a43448d77705b2b07e1758ffe8035aa6ba146abc2167984e8cb0f1615797b341")
        version("5.1.0", sha256="6a758f5a8332e6774cd8e14a4e5ce05e43b1e05298d817b4068c35fa1793d333")

    depends_on("cmake@3:", type="build")
    depends_on("rsync")

    for ver in [
        "5.1.0",
        "5.1.3",
        "5.2.0",
        "5.2.1",
        "5.2.3",
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
        "5.5.0",
        "5.5.1",
    ]:
        depends_on(f"comgr@{ver}", type="link", when=f"@{ver}")
        depends_on(f"hsa-rocr-dev@{ver}", type="link", when=f"@{ver}")
        depends_on("elf", type="link", when=f"@{ver}")

    for ver in ["5.5.0", "5.5.1"]:
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")

    root_cmakelists_dir = "src"

    # Reset the installation path and remove direct reference to rsync.
    patch("0002-Remove-usr-bin-rsync-reference-5.2.0.patch", when="@5.0.2:5.2.0")
    # Remove direct reference to /usr/bin/rsync path for rsync command
    patch(
        "0002-Remove-direct-reference-to-usr-bin-rysnc-for-rsync-cmd-5.2.1.patch", when="@5.2.1:"
    )

    def cmake_args(self):
        args = [self.define("ROCM_VERSION", self.spec.version)]
        return args

    @run_after("install")
    def install_stub(self):
        install("include/atmi_interop_hsa.h", self.prefix.include)
