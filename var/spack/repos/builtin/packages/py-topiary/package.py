# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTopiary(PythonPackage):
    """Python framework for doing ancestral sequence reconstruction."""

    homepage = "https://github.com/harmslab/topiary"

    url = "https://github.com/harmslab/topiary/archive/refs/tags/v0.9.9.tar.gz"
    git = "https://github.com/harmslab/topiary.git"

    maintainers("snehring")

    version("main", branch="main")
    version("0.9.9", sha256="5601fba92e7add33a3732482426b2c7ef46b0fccc4a4ea11357537e1b937903c")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type="run")
    depends_on("py-pandas", type="run")
    depends_on("py-matplotlib", type="run")
    depends_on("py-ete3", type="run")
    depends_on("py-toytree", type="run")
    depends_on("py-dendropy", type="run")
    depends_on("py-pastml", type="run")
    depends_on("py-opentree", type="run")
    depends_on("py-tqdm", type="run")
    depends_on("py-mpi4py", type="run")

    depends_on("blast-plus", type="run")
    depends_on("muscle5@5.0:", type="run")
    depends_on("generax@2.0:+mpi", type="run")
    depends_on("raxml-ng@1.1:", type="run")

    depends_on("mpi", type="run")
    depends_on("openmpi+legacylaunchers", type="run", when="^openmpi schedulers=slurm")

    conflicts("mpich")

    def patch(self):
        if self.spec.satisfies("^raxml-ng+mpi"):
            filter_file(
                r"RAXML_BINARY\s*=\s*\"raxml-ng\"$",
                'RAXML_BINARY = "raxml-ng-mpi"',
                "topiary/raxml/_raxml.py",
            )
            filter_file(
                r"binary\s*=\s*\"raxml-ng\"",
                'binary = "raxml-ng-mpi"',
                "topiary/_private/installed.py",
            )
