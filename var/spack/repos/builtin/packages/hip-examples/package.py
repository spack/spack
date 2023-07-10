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
    patch("0002-add-fpic-compile-to-add4.patch")
    depends_on("hip")
    depends_on("rocm-openmp-extras")

    def install(self, spec, prefix):
        stage = os.getcwd()
        os.environ["ROCM_OPENMP_EXTRAS_DIR"] = self.spec["rocm-openmp-extras"].prefix
        os.environ["LD_LIBRARY_PATH"] = self.spec["rocm-openmp-extras"].prefix.lib
        for root, dirs, files in os.walk(stage):
            if "Makefile" in files:
                with working_dir(root, create=True):
                    make()
                    # itterate through the files in dir to find the newly built binary
                    for file in os.listdir("."):
                        if file not in files and os.path.isfile(file) and os.access(file, os.X_OK):
                            install(file, join_path(prefix, file))
                            if file == "RecursiveGaussian":
                                install(
                                    "RecursiveGaussian_Input.bmp",
                                    join_path(prefix, "RecursiveGaussian_Input.bmp"),
                                )

    def test_examples(self):
        """
        run all hip example binaries
        """

        os.environ["LD_LIBRARY_PATH"] = self.spec["rocm-openmp-extras"].prefix.lib
        test_dir = self.prefix
        for file_name in os.listdir(test_dir):
            file_path = join_path(test_dir, file_name)
            if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                with test_part(
                    self,
                    "test_example_{0}".format(file_name),
                    purpose="run installed {0}".format(file_name),
                ):
                    exe = which(file_path)
                    exe()
