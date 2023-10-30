# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Moose(MakefilePackage):
    """The Multiphysics Object-Oriented Simulation Environment (MOOSE)
    is a finite-element, multiphysics framework primarily developed by
    Idaho National Laboratory. It provides a high-level interface to
    some of the most sophisticated nonlinear solver technology on the
    planet. MOOSE presents a straightforward API that aligns well with
    the real-world problems scientists and engineers need to
    tackle. Every detail about how an engineer interacts with MOOSE
    has been thought through, from the installation process through
    running your simulation on state of the art supercomputers, the
    MOOSE system will accelerate your research."""

    git = "https://github.com/idaholab/moose"
    url = "https://github.com/idaholab/moose/archive/refs/tags/2022-06-10.tar.gz"
    version(
        "2022-06-10", sha256="1d3c031d7fd3179d04985272a7d7a650c39e0d450c828d1502354e555e7e2fe3"
    )

    variant("gui", default=False, description="build with gui (peacock)")

    depends_on(
        "petsc@3.16.6+metis+ptscotch+strumpack+scalapack+mumps+superlu-dist+openmp+int64+hypre"
    )
    depends_on("scotch@6.1.1")
    depends_on("hypre@2.23+int64+openmp")
    depends_on("slepc~arpack")
    # libmesh pin from docker_ci/Dockerfile
    depends_on(
        "libmesh@git.5a7a9bd0e7295628f465c3bb4e42563b8b8c1a9c=1.7.0+metis+fparser+petsc+exodusii+metaphysicl+nanoflann+unique+nemesis+hdf5+eigen+boost+gmv+libhilbert+qhull~warnings+xdr+vtk threads=openmp",  # noqa: E501
        when="@2022-06-10",
    )
    depends_on("eigen")
    depends_on("cmake", type="build")
    depends_on("mpi")
    depends_on("patchelf", type="build")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))

    depends_on("py-pyqt5", type=("build", "run"), when="+gui")
    depends_on("vtk+python", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))

    extends("python")

    def setup_build_environment(self, env):
        env.set("PETSC_DIR", self.spec["petsc"].prefix)
        env.set("SLEPC_DIR", self.spec["slepc"].prefix)
        env.set("LIBMESH_DIR", self.spec["libmesh"].prefix)
        env.set("MOOSE_DIR", self.prefix)
        env.set("MOOSE_SKIP_DOCS", "True")

    def setup_run_environment(self, env):
        env.set("LIBMESH_DIR", self.spec["libmesh"].prefix)
        env.set("MOOSE_DIR", self.prefix)
        env.append_path("PATH", self.prefix.scripts)
        env.append_path("PYTHONPATH", self.prefix.python)

    def build(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)
        with working_dir(join_path(prefix, "framework")):
            make()
        with working_dir(join_path(prefix, "test")):
            make()
        with working_dir(join_path(prefix, "modules")):
            make("all", "builds")
        with working_dir(join_path(prefix, "modules", "module_loader")):
            make("LIBRARY_SUFFIX=yes", "SUFFIX=")

    def install(self, spec, prefix):
        pass

    def check(self):
        with working_dir(join_path(self.prefix, "modules")):
            make("test")
        with working_dir(join_path(self.prefix, "test")):
            make("test")

    def installcheck(self):
        pass
