# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class OtfCpt(CMakePackage):
    """Tool to collect and report model factors (aka. fundamental performance factors)
    for hybrid MPI + OpenMP applications on-the-fly."""

    # Add a proper url for your package's homepage here.
    homepage = (
        "https://github.com/RWTH-HPC/OTF-CPT?tab=readme-ov-file#on-the-fly-critical-path-tool"
    )
    git = "https://github.com/RWTH-HPC/OTF-CPT.git"

    maintainers("jgraciahlrs", "jprotze")

    license("Apache-2.0", checked_by="jgracia")

    version("0.9", tag="v0.9")

    depends_on("cxx", type="build")
    depends_on("mpi")
    conflicts(
        "%gcc",
        msg="GCC compilers currently do not support OMPT, please use a clang-like compiler.",
    )

    patch(
        "https://github.com/RWTH-HPC/OTF-CPT/commit/b58f83588a4c231b71ca48dcddd909e1ab318cc6.diff",
        sha256="1c8e1c4b5bf4cd1c6e4ed9a9d8c5ef47abe2aad5402ec466db0df4f96cbd3407",
        when="@0.9",
    )
