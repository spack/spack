# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAlphafoldColabfold(PythonPackage, CudaPackage):
    """An implementation of the inference pipeline of AlphaFold v2.3.1.
    This is a completely new model that was entered as AlphaFold2 in CASP14
    and published in Nature. This package contains patches for colabfold."""

    homepage = "https://pypi.org/project/alphafold-colabfold/#description"
    pypi = "alphafold-colabfold/alphafold-colabfold-2.3.5.tar.gz"
    git = "https://github.com/sokrypton/alphafold"

    version("latest", branch="main")
    version("2.3.5", sha256="92a01f96851b4c2897c3fc1a083dc215cffe318ab06bdbb3186b7d41a5e72e4b")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.10", type=("build", "run"))
    depends_on("py-absl-py@1.0.0:", type=("build", "run"))
    depends_on("py-biopython@1.79:", type=("build", "run"))
    depends_on("py-chex", type=("build", "run"))
    depends_on("py-dm-haiku", type=("build", "run"))
    depends_on("py-dm-tree@0.1.8", type=("build", "run"))
    depends_on("py-docker@5.0.0", type=("build", "run"))
    depends_on("py-immutabledict@2.0.0:", type=("build", "run"))
    depends_on("py-jax@0.4.14", type=("build", "run"))
    depends_on("py-ml-collections@0.1.0", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-tensorflow@2.11 +cuda", type=("build", "run"), when="+cuda")
    depends_on("py-tensorflow@2.11", type=("build", "run"))
    depends_on("py-pdbfixer@1.8.1", type=("build", "run"))
    depends_on("openmm@7.7.0", type=("build", "run"))
    depends_on("openmm@7.7.0 +cuda", type=("build", "run"), when="+cuda")

    patch(
        url_or_filename="https://github.com/sokrypton/alphafold/commit/1f04253c620703d6768b20987b3b5e075314095f.patch",
        sha256="b29d56b236e65ae609b7e4edf7e72c2b9a3a7ff048c9939950cab12192ca0e43",
        when="@2.3.5 ^jax@0.3.26:"
    )
