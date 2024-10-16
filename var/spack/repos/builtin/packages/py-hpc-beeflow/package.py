# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyHpcBeeflow(PythonPackage):
    """BEE is a workflow orchestration system designed to build containerized 
      HPC applications and orchestrate workflows across HPC and cloud systems. 
      BEE has adopted the Common Workflow Language (CWL) for specifying workflows. 
      Complex scientific workflows specified by CWL are managed and visualized 
      through a graph database, giving the user the ability to monitor the state 
      of each task in the workflow. BEE runs jobs using the workload scheduler 
      (i.e. Slurm or Flux) on the HPC system that tasks are 
      specified to run on."""

    pypi = "hpc-beeflow/hpc_beeflow-0.1.9.tar.gz"

    license("MIT")
    maintainers("aquan9")

    version("0.1.9", sha256="196eb9155a5ca6e35d0cc514e0609cf352fc757088707306653496b83a311ac1")
    version("0.1.8", sha256="7ffc7f2a6e6c4892b9432ba939ee7179d1189cedf82382752a3c268d70fceddd")

    depends_on("py-poetry@1.6.1:", type="build")
    depends_on("neo4j@5.17.0:", type=("run"))
    depends_on("redis@7.4.0:", type=("run"))

    depends_on("python@3.12.2:", type=("build", "run"))
