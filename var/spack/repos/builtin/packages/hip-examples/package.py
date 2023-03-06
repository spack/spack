# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class HipExamples(Package):
    """Examples for HIP"""

    homepage = "https://github.com/ROCm-Developer-Tools/HIP-Examples/"
    git = "https://github.com/ROCm-Developer-Tools/HIP-Examples.git"
    url = "https://github.com/ROCm-Developer-Tools/HIP-Examples/archive/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath", "afzpatel")

    version("master", branch="master")

    version("5.4.3", sha256="053b8b7892e2929e3f90bd978d8bb1c9801e4803eadd7d97fc6692ce60af1d47")

    patch("0001-add-inc-and-lib-paths-to-openmp-helloworld.patch")
    depends_on("hip")
    depends_on("rocm-openmp-extras")
    depends_on("cmake", type="build")

    def install(self, spec, prefix):
        stage = os.getcwd()

        for root, dirs, files in os.walk(stage):
            if "Makefile" in files or "CMakeLists.txt" in files:
                with working_dir(root, create=True):
                    if "CMakeLists.txt" in files:
                        cmake("-DROCM_OPENMP_EXTRAS_DIR=" + self.spec["rocm-openmp-extras"].prefix)
                    make()
                    # itterate through the files in dir to find the newly built binary
                    for file in os.listdir("."):
                        if file not in files and os.path.isfile(file) and os.access(file, os.X_OK):
                            install(file, join_path(prefix, file))
