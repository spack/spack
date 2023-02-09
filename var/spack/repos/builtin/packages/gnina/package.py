# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
import os


class Gnina(CMakePackage, CudaPackage):
    """gnina (pronounced NEE-na) is a molecular docking program with integrated support
    for scoring and optimizing ligands using convolutional neural networks."""

    homepage = "https://github.com/gnina/gnina"
    url = "https://github.com/gnina/gnina/archive/refs/tags/v1.0.2.tar.gz"
    git = "https://github.com/gnina/gnina.git"

    maintainers("RMeli")

    version("master", branch="master")

    depends_on("git", type="build")  # libmolgrid

    _boost = "boost" + "".join(
        [
            "+atomic",
            "+chrono",
            "+date_time",
            "+exception",
            "+filesystem",
            "+graph",
            "+iostreams",
            "+locale",
            "+log",
            "+math",
            "+python",
            "+program_options",
            "+random",
            "+regex",
            "+serialization",
            "+signals",
            "+system",
            "+test",
            "+thread",
            "+timer",
            "+wave",
        ]
    )

    depends_on("zlib")
    depends_on(_boost)
    depends_on("glog")
    depends_on("protobuf")
    depends_on("hdf5+cxx+hl")
    depends_on("openblas~fortran")

    depends_on("libmolgrid")

    depends_on("openbabel@3:~gui~cairo~maeparser~coordgen")
    depends_on("rdkit")

    depends_on("python", type="build")
    depends_on("py-numpy", type="build")
    depends_on("py-pytest", type="build")

    depends_on("cuda@11")

    def cmake_args(self):
        args = [
            "-DBLAS=Open",  # Use OpenBLAS instead of Atlas' BLAS
        ]
        return args
