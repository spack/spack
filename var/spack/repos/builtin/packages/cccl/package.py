# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cccl(CMakePackage):
    """C++ building blocks that make it easier to write safe and efficient CUDA
    code. Contains libraries such as Thrust, CUB, and libcudacxx."""

    homepage = "https://github.com/NVIDIA/cccl"
    url = "https://github.com/NVIDIA/cccl/archive/refs/tags/v2.2.0.tar.gz"

    maintainers("stephenswat")

    license("Apache-2.0", checked_by="stephenswat")

    version("2.4.0", sha256="2368db9440fbd302450424c624d7f885529ba0e6c96eb4076aa4412c436b2359")
    version("2.3.2", sha256="7251733c68a05bcb9671dfb0d37e55a5219843d5ba88370234e28bb3c98d545c")
    version("2.3.1", sha256="26c91f3652ddd33d0b2b1802301295812a2fc98f33018506bbc35869bfbb91b8")
    version("2.3.0", sha256="922c9e72a7d6d91ef6a1421f2545a947529a179d307853be1b1615c02241c271")
    version("2.2.0", sha256="e27678a9d583f9994e591367e864425e722050a9ee1d721b2bd736b442b768d4")

    depends_on("cuda@11.1:")

    def cmake_args(self):
        args = [
            self.define("CCCL_ENABLE_TESTING", False),
            self.define("CCCL_ENABLE_EXAMPLES", False),
            self.define("LIBCUDACXX_ENABLE_LIBCUDACXX_TESTS", False),
            self.define("THRUST_ENABLE_HEADER_TESTING", False),
            self.define("THRUST_ENABLE_TESTING", False),
            self.define("THRUST_ENABLE_EXAMPLES", False),
            self.define("THRUST_ENABLE_BENCHMARKS", False),
            self.define("CUB_ENABLE_HEADER_TESTING", False),
            self.define("CUB_ENABLE_TESTING", False),
            self.define("CUB_ENABLE_BENCHMARKS", False),
            self.define("CUB_ENABLE_TUNING", False),
            self.define("CUB_ENABLE_EXAMPLES", False),
        ]

        return args
