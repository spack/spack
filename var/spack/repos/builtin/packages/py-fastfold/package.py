# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFastfold(PythonPackage):
    """Optimizing Protein Structure Prediction Model Training and Inference on
    GPU Clusters."""

    homepage = "https://github.com/hpcaitech/FastFold"
    url = "https://github.com/hpcaitech/FastFold/archive/refs/tags/0.2.0.tar.gz"

    maintainers = ["meyersbs"]

    version('0.2.0', sha256='6760dbae9809b8b26219c9477489d34325807be504098901d0375fbdc3103f88')

    # From README:
    depends_on("python@3.8:3.9",                type=("build", "run"))
    depends_on("cuda@11.1:",                    type=("build", "run"))
    depends_on("py-torch@1.10:+cuda",           type=("build", "run"))
    # From setup.py:
    depends_on("py-setuptools",                 type="build")
    depends_on("py-einops",                     type=("build", "run"))
    depends_on("py-colossalai",                 type=("build", "run"))
    # From environment.yml (to appease import errors):
    depends_on("py-scipy@1.7.1",                type="run")
    depends_on("py-dm-tree@0.1.6",              type="run")
    depends_on("py-biopython@1.79",             type="run")
    depends_on("py-ml-collections@0.1.0:",      type="run")  # Requirement relaxed (was @0.1.0)
    depends_on("py-ray@2.0.0:",                 type="run")  # Requirement relaxed (was @2.0.0)
    depends_on("py-pandas",                     type="run")
    depends_on("openmm@7.7.0:+cuda",            type="run")
    depends_on("py-requests@2.26.0",            type="run")
    # From import errors:
    depends_on("py-setproctitle",               type="run")
    depends_on("py-pdbfixer",                   type="run")
    depends_on("py-pytorch-lightning",          type="run")
