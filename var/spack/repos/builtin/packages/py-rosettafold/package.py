# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
from spack.package import *


class PyRosettafold(PythonPackage, CudaPackage):
    """https://github.com/RosettaCommons/RoseTTAFold"""

    homepage = "https://github.com/RosettaCommons/RoseTTAFold"
    url = "https://github.com/RosettaCommons/RoseTTAFold/archive/refs/tags/v1.1.0.tar.gz"

    variant("cuda", default=True, description="Accelerate with GPU")

    version("1.1.0", sha256="55706a815a137a7f4f51370e20456a96620d0bd168a889560fd06ad890ce3ea3")
    
    depends_on("py-setuptools@52.0.0", type="build")
    depends_on("python@3.8", type=("build", "run"))
    depends_on("hh-suite@3.3.0", type="run")
    depends_on("py-biopython@1.78", type="run")
    depends_on("csblast@2.2.3", type="run")
    depends_on("cuda@11", type="run")
    depends_on("blast-legacy@2.2.26", type="run")
    depends_on("blas", type="run")
    depends_on("py-intel-openmp@2021.2.0", type="run")
    depends_on("py-numpy@1.20.2", type="run")
    depends_on("py-pandas@1.2.5", type="run")
    depends_on("psipred@4.0", type="run")
    depends_on("py-torch@1.9.0 +cuda cuda_arch=70,75,80,86", type="run", when="+cuda")
    depends_on("py-torch@1.9.0", type="run")
    depends_on("py-torch-cluster@1.5.9", type="run")
    depends_on("py-torch-geometric@1.7.2", type="run")
    depends_on("py-torch-scatter@2.0.7", type="run")
    depends_on("py-torch-sparse@0.6.10", type="run")
    depends_on("py-torch-spline-conv@1.2.1", type="run")
    depends_on("py-scikit-learn@0.24.2", type="run")
    depends_on("py-dgl@0.6.1", type="run")
    depends_on("py-scipy@1.7.0", type="run")
    depends_on("py-tqdm", type="run")

    resource(
        name="weights",
        url=f"file://{os.getcwd()}/weights.tar.gz", # url="https://files.ipd.uw.edu/pub/RoseTTAFold/weights.tar.gz"
        sha256="4c883ffbfc98623750a1ced177fa35796b7d55cf3945f3d74ce040d65c804b28",
        placement="weights"
    )

    def install(self, spec, prefix):
        install_tree(".", prefix)
