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

    version("1.5.3", sha256="1b2776f285981796559effbc3691ebbcfcde68514cc05559583ebab76c4c25e8")

    variant("jax", default=True, description="Install with Jax")
    variant("alphafold_colabfold", default=True, description="Install with py-alphafold-colabfold")

    # Inspired by the meta.yaml file of the corresponding Conda environment available here:
    # https://anaconda.org/bioconda/colabfold/1.5.3/download/noarch/colabfold-1.5.3-pyh7cba7a3_1.tar.bz2

    patch(
        "fix-jax-04-nan.patch",
        when="1.5.3",
        sha256="6244c2143987dd4a6a87c1174c7a801c220034fbeb8d13f901b0f950b69d8543",
    )

    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="Must specify CUDA compute capabilities of your GPU, see "
        "https://developer.nvidia.com/cuda-gpus",
    )

    depends_on("py-poetry-core@1.8.1", type="build")
    depends_on("py-poetry@1.7", type="build")
    depends_on("python@3.7.1:3.10", type=("build", "run"))

    depends_on("py-absl-py@1.4:", type=("build", "run"))
    depends_on("py-jax@0.4.14", when="+jax", type=("build", "run"))
    depends_on(
        f"py-jaxlib@0.4.14 +cuda",
        when="+jax +cuda",
        type=("build", "run")
    )
    depends_on("py-jaxlib@0.4.14", when="+jax", type=("build", "run"))
    depends_on("py-alphafold-colabfold@2.3.5 +cuda",
        when="+alphafold_colabfold +cuda",
        type=("build", "run")
    )
    depends_on("py-alphafold-colabfold@2.3.5", when="+alphafold_colabfold", type=("build", "run"))
    depends_on("py-matplotlib@3.2.2:3", type=("build", "run"))
    # Tensorflow is always without cuda
    depends_on("py-tensorflow@2.12.1 ~cuda", type=("build", "run"))
    depends_on("py-numpy@1.21.6:", type=("build", "run"))
    depends_on("py-pandas@1.3.4:", type=("build", "run"))
    depends_on("py-requests@2.26.0:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-appdirs@1.4.4:", type=("build", "run"))
    depends_on("py-py3dmol@2.0.1:", type=("build", "run"))
    depends_on("py-dm-haiku", type=("build", "run"))
    depends_on("py-importlib-metadata@4.8.2:4", type=("build", "run"))
