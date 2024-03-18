# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.hooks.sbang import filter_shebang
from spack.package import *


class Hipcc(CMakePackage):
    """HIPCC: HIP compiler driver"""

    homepage = "https://github.com/ROCm/hipcc"
    git = "https://github.com/ROCm/hipcc.git"
    url = "https://github.com/ROCm/HIPCC/archive/refs/tags/rocm-6.0.2.tar.gz"

    maintainers("srekolam", "renjithravindrankannath", "afzpatel")

    license("MIT")

    version("6.0.2", sha256="d6209b14fccdd00d7231dec4b4f962aa23914b9dde389ba961370e8ba918bde5")
    version("6.0.0", sha256="e9cfaaecaf0e6ed363946439197f340c115e8e1189f96dbd716cf20245c29255")
    version("5.7.1", sha256="d47d27ef2b5de7f49cdfd8547832ac9b437a32e6fc6f0e9c1646f4b704c90aee")
    version("5.7.0", sha256="9f839bf7226e5e26f3150f8ba6eca507ab9a668e68b207736301b3bb9040c973")

    depends_on("numactl")

    patch("0014-remove-compiler-rt-linkage-for-host.6.0.patch", when="@6.0:")

    def patch(self):
        numactl = self.spec["numactl"].prefix.lib
        with working_dir("bin"):
            filter_shebang("hipconfig")
        with working_dir("src"):
            filter_file(" -lnuma", f" -L{numactl} -lnuma", "hipBin_amd.h")
