# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class HpcBeeflow(PythonPackage):
    """BEE is a workflow orchestration system designed to build containerized
    HPC applications and orchestrate workflows across HPC and cloud systems.
    BEE has adopted the Common Workflow Language (CWL) for specifying workflows.
    Complex scientific workflows specified by CWL are managed and visualized
    through a graph database, giving the user the ability to monitor the state
    of each task in the workflow. BEE runs jobs using the workload scheduler
    (i.e. Slurm or Flux) on the HPC system that tasks are
    specified to run on."""

    homepage = "https://github.com/lanl/bee"
    pypi = "hpc_beeflow/hpc_beeflow-0.1.10.tar.gz"
    git = "https://github.com/lanl/BEE.git"

    maintainers("pagrubel")

    tags = ["e4s"]

    license("MIT")

    version("spack-develop", branch="spack-develop")
    version("0.1.10", sha256="b7863798e15591a16f6cd265f9b5b7385779630f1c37d8a2a5178b8bf89fc664")

    depends_on("neo4j@5.17.0", type=("build", "run"))
    depends_on("redis@7.4.0", type=("build", "run"))

    depends_on("python@3.8.3:3.13.0", type=("build", "run"))
    depends_on("py-poetry@0.12:", type="build")

    depends_on("py-flask@2.0:", type=("build", "run"))
    depends_on("py-fastapi@0.109.2", type=("build", "run"))
    depends_on("py-uvicorn@0.27.1", type=("build", "run"))
    depends_on("py-neo4j@5:", type=("build", "run"))
    depends_on("py-pyyaml@6.0.1:", type=("build", "run"))
    depends_on("py-flask-restful@0.3.9", type=("build", "run"))
    depends_on("py-cwl-utils@0.16", type=("build", "run"))
    depends_on("py-apscheduler@3.6.3:", type=("build", "run"))
    depends_on("py-jsonpickle@2.2.0:", type=("build", "run"))
    depends_on("py-requests@2.32.3:", type=("build", "run"))
    depends_on("py-requests-unixsocket@0.4.1:", type=("build", "run"))
    depends_on("py-python-daemon@2.3.1:", type=("build", "run"))
    depends_on("py-gunicorn@20.1.0:22", type=("build", "run"))
    depends_on("py-typer@0.5.0", type=("build", "run"))
    depends_on("py-cffi@1.15.1:", type=("build", "run"))
    depends_on("py-celery+redis+sqlalchemy@5.3.4:", type=("build", "run"))
    depends_on("py-docutils@0.18.1", type=("build", "run"))
    depends_on("py-graphviz@0.20.3:", type=("build", "run"))
    depends_on("py-networkx@3.1", type=("build", "run"))
    depends_on("py-pre-commit@3.5.0", type=("build", "run"))
    depends_on("py-mypy-extensions", type=("build", "run"))

    # Setup for when "no containers" is specified
    def setup_run_environment(self, env):

        neo4j_bin = join_path(self.spec["neo4j"].prefix, "packaging/standalone/target")
        redis_bin = join_path(self.spec["redis"].prefix, "bin")

        env.prepend_path("PATH", neo4j_bin)
        env.prepend_path("PATH", redis_bin)

        env.set("neo4j_path", neo4j_bin)
        env.set("redis_path", redis_bin)
