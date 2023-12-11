# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyColabfold(PythonPackage, CudaPackage):
    """Making Protein folding accessible to all!"""

    homepage = "https://github.com/sokrypton/ColabFold"

    url = "https://github.com/sokrypton/ColabFold/archive/refs/tags/v1.5.2.tar.gz"
    git = "https://github.com/sokrypton/ColabFold"

    version("1.5.3", branch="main", commit="ca6b297021bb876157b75d84d591ed350cbece85")
    version(
        "1.5.2",
        sha256="b3b82e831e241a6ab40f2b0c6d560ac5328c6a0b505a0186c75e397ca1a16477"
    )

    variant("jax", default=True, description="Install with Jax")
    variant("alphafold_colabfold", default=True, description="Install with py-alphafold-colabfold")

    depends_on("py-poetry-core@1", type="build")

    depends_on("python@3.7.1:3.10", type=("build", "run"))

    depends_on("py-absl-py@1", type=("build", "run"))
    depends_on("py-jax@0.3.25:", type=("build", "run"), when="+jax")
    depends_on("py-matplotlib@3.2.2:", type=("build", "run"))
    depends_on("py-tensorflow@2.11.0:", type=("build", "run"))
    depends_on("py-tensorflow@2.11.0: +cuda", type=("build", "run"), when="+cuda")
    depends_on("py-numpy@1.21.6:", type=("build", "run"))
    depends_on("py-pandas@1.3.4:", type=("build", "run"))
    depends_on("py-alphafold-colabfold@2.3.5", type=("build", "run"), when="+alphafold_colabfold")
    depends_on("py-requests@2.26.0:", type=("build", "run"))
    depends_on("py-tqdm@4.62.2:", type=("build", "run"))
    depends_on("py-appdirs@1.4.4:", type=("build", "run"))
    depends_on("py-py3dmol@2.0.1:", type=("build", "run"))
    depends_on("py-dm-haiku@0.0.9", type=("build", "run"))
    depends_on("py-importlib-metadata@4.8.2:4", type=("build", "run"))
