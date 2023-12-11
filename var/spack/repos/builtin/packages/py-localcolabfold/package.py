# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyLocalcolabfold(PythonPackage, CudaPackage):
    """LocalColabFold is an installer script designed to make ColabFold
    functionality available on users' local machines."""

    homepage = "https://github.com/YoshitakaMo/localcolabfold"

    url = "https://github.com/YoshitakaMo/localcolabfold/archive/refs/tags/v1.5.2.tar.gz"

    version("1.5.2", sha256="b3b82e831e241a6ab40f2b0c6d560ac5328c6a0b505a0186c75e397ca1a16477")

    depends_on("py-pip", type="build")

    depends_on("python@3.10", type=("build", "run"))

    depends_on("cuda@11.6.0", type=("build", "run"))
    depends_on("cudnn@8.2.1.32", type=("build", "run"))
    depends_on("openmm@7.7.0", type=("build", "run"))
    depends_on("py-pdbfixer@1.7", type=("build", "run"))
    depends_on("py-colabfold@1.5.3 ~jax", type=("build", "run"))
    depends_on("kalign2@2.0.3", type=("build", "run"))
    depends_on("hh-suite@3.3.0", type=("build", "run"))
    depends_on("mmseqs2@14.7e284", type=("build", "run"))
    depends_on("py-colabfold@1.5.3", type=("build", "run"))
    depends_on("py-alphafold-colabfold@2.3.5", type=("build", "run"))
    depends_on("py-jax@0.3.25", type=("build", "run"))
    depends_on("py-chex@0.1.6", type=("build", "run"))
    depends_on("py-biopython@1.79", type=("build", "run"))

    def patch(self):
        filter_file("from matplotlib import pyplot as plt", "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt", "colabfold/plot.py")
        filter_file("appdirs.user_cache_dir(__package__ or \"colabfold\")", f"\"{self.prefix}/colabfold\"", "colabfold/download.py")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.bin)

    @run_after("install")
    def download_weights(self):
        spec = self.spec
        python = spec["python"].command
        python("-m", "colabfold.download")
