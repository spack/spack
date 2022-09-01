# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *

class MlperfOpencatalyst(PythonPackage, CudaPackage):
    """Reference implementation for the MLPerf HPC OpenCatalyst DimeNet++ benchmark"""

    homepage = "https://opencatalystproject.org/"
    git = "https://github.com/mlcommons/hpc.git"
    
    version("main", branch="main")
    
    tags = ["proxy-app"]
    
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-ase@3.21:3.21.9999", type=("build", "run"))
    depends_on("py-matplotlib@3.3:3.3.9999", type=("build", "run"))
    depends_on("py-pre-commit@2.10:2.10.9999", type=("build", "run"))
    depends_on("py-pymatgen@2020.12.31", type=("build", "run"))
    depends_on("py-torch@1.8.1", type=("build", "run"))
    depends_on("py-pyyaml@5.4:5.4.9999", type=("build", "run"))
    depends_on("py-tensorboard@2.4:2.4.9999", type=("build", "run"))
    depends_on("py-tqdm@4.58:4.58.9999", type=("build", "run"))
    depends_on("py-sphinx", type=("build", "run"))
    depends_on("py-nbsphinx", type=("build", "run"))
    # TODO: Does pandoc work or do we need to make a py-pandoc?
    depends_on("py-black", type=("build", "run"))
    depends_on("py-torch+cuda", when="+cuda", type=("build", "run"))
    depends_on("py-torch~cuda", when="~cuda", type=("build", "run"))
    depends_on("py-torch-scatter+cuda", when="+cuda", type=("build", "run"))
    depends_on("py-torch-scatter~cuda", when="~cuda", type=("build", "run"))
    depends_on("py-torch-spline-conv+cuda", when="+cuda", type=("build", "run"))
    depends_on("py-torch-spline-conv~cuda", when="~cuda", type=("build", "run"))


    @property
    def build_directory(self):
        return "open_catalyst"

