# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.filesystem as fs

from spack.package import *


class Nektar(CMakePackage):
    """Nektar++: Spectral/hp Element Framework"""

    homepage = "https://www.nektar.info/"
    git = "https://gitlab.nektar.info/nektar/nektar.git"

    version("5.5.0", commit="4365d5d7156139f238db962deae5eb25e0437d12", preferred=True)
    version("5.4.0", commit="002bf62648ec667e10524ceb8a98bb1c21804130")
    version("5.3.0", commit="f286f809cfeb26cb73828c90a689a048898971d2")

    variant("mpi", default=True, description="Builds with mpi support")
    variant("fftw", default=True, description="Builds with fftw support")
    variant("arpack", default=True, description="Builds with arpack support")
    variant("tinyxml", default=True, description="Builds with external tinyxml support")
    variant("hdf5", default=True, description="Builds with hdf5 support")
    variant("scotch", default=False, description="Builds with scotch partitioning support")
    variant("demos", default=False, description="Build demonstration codes")
    variant("python", default=True, description="Enable python support")
    # Solver variants
    variant(
        "acoustic_solver",
        default=False,
        description="Builds an executable associated with the Acoustic solver",
    )
    variant(
        "adr_solver",
        default=False,
        description="Builds an executable associated with the ADR solver",
    )
    variant(
        "cardiac_solver",
        default=False,
        description="Builds an executable associated with the Cardiac electrophysiology solver",
    )
    variant(
        "compflow_solver",
        default=False,
        description="Builds an executable associated with the CompressibleFlow solver",
    )
    variant(
        "diff_solver",
        default=False,
        description="Builds an executable associated with the Diffusion solver",
    )
    variant(
        "dummy_solver",
        default=False,
        description="Builds an executable associated with the Dummy solver",
    )
    variant(
        "elasticity_solver",
        default=False,
        description="Builds an executable associated with the Elasticity solver",
    )
    variant(
        "imgwarp_solver",
        default=False,
        description="Builds an executable associated with the Image Warping solver",
    )
    variant(
        "ins_solver",
        default=False,
        description="Builds an executable associated with the Incompressible Navier Stokes solver",
    )
    variant(
        "mmf_solver",
        default=False,
        description="Builds an executable associated with the MMF solver",
    )
    variant(
        "pulsewave_solver",
        default=False,
        description="Builds an executable associated with the Pulse Wave solver",
    )
    variant(
        "shwater_solver",
        default=False,
        description="Builds an executable associated with the Shallow Water solver",
    )
    variant(
        "vortexwave_solver",
        default=False,
        description="Builds an executable associated with the Vortex Wave solver",
    )

    depends_on("cmake@2.8.8:", type="build", when="~hdf5")
    depends_on("cmake@3.2:", type="build", when="+hdf5")

    depends_on("blas")
    depends_on("zlib")
    depends_on("tinyxml", when="+tinyxml")
    depends_on("lapack")
    depends_on(
        "boost@1.74.0: +thread +iostreams +filesystem +system +program_options +regex +pic"
        "+python +numpy",
        when="+python",
    )
    depends_on(
        "boost@1.74.0: +thread +iostreams +filesystem +system +program_options +regex +pic",
        when="~python",
    )
    depends_on("tinyxml", when="platform=darwin")

    depends_on("mpi", when="+mpi", type=("build", "link", "run"))
    depends_on("fftw@3.0: +mpi", when="+mpi+fftw")
    depends_on("fftw@3.0: ~mpi", when="~mpi+fftw")
    depends_on("arpack-ng +mpi", when="+arpack+mpi")
    depends_on("arpack-ng ~mpi", when="+arpack~mpi")
    depends_on("hdf5 +mpi +hl", when="+mpi+hdf5")
    depends_on("scotch ~mpi ~metis", when="~mpi+scotch")
    depends_on("scotch +mpi ~metis", when="+mpi+scotch")

    extends("python@3:", when="+python")

    conflicts("+hdf5", when="~mpi", msg="Nektar's hdf5 output is for parallel builds only")

    def cmake_args(self):
        args = []

        def hasfeature(feature):
            return "ON" if feature in self.spec else "OFF"

        args.append("-DNEKTAR_BUILD_DEMOS=%s" % hasfeature("+demos"))
        args.append("-DNEKTAR_BUILD_PYTHON=%s" % hasfeature("+python"))
        args.append("-DNEKTAR_BUILD_SOLVERS=ON")
        args.append("-DNEKTAR_BUILD_UTILITIES=ON")
        args.append("-DNEKTAR_ERROR_ON_WARNINGS=OFF")
        args.append("-DNEKTAR_SOLVER_ACOUSTIC=%s" % hasfeature("+acoustic_solver"))
        args.append("-DNEKTAR_SOLVER_ADR=%s" % hasfeature("+adr_solver"))
        args.append("-DNEKTAR_SOLVER_CARDIAC_EP=%s" % hasfeature("+cardiac_solver"))
        args.append("-DNEKTAR_SOLVER_COMPRESSIBLE_FLOW=%s" % hasfeature("+compflow_solver"))
        args.append("-DNEKTAR_SOLVER_DIFFUSION=%s" % hasfeature("+diff_solver"))
        args.append("-DNEKTAR_SOLVER_DUMMY=%s" % hasfeature("+dummy_solver"))
        args.append("-DNEKTAR_SOLVER_ELASTICITY=%s" % hasfeature("+elasticity_solver"))
        args.append("-DNEKTAR_SOLVER_IMAGE_WARPING=%s" % hasfeature("+imgwarp_solver"))
        args.append("-DNEKTAR_SOLVER_INCNAVIERSTOKES=%s" % hasfeature("+ins_solver"))
        args.append("-DNEKTAR_SOLVER_MMF=%s" % hasfeature("+mmf_solver"))
        args.append("-DNEKTAR_SOLVER_PULSEWAVE=%s" % hasfeature("+pulsewave_solver"))
        args.append("-DNEKTAR_SOLVER_SHALLOW_WATER=%s" % hasfeature("+shwater_solver"))
        args.append("-DNEKTAR_SOLVER_VORTEXWAVE=%s" % hasfeature("+vortexwave_solver"))
        args.append("-DNEKTAR_USE_ARPACK=%s" % hasfeature("+arpack"))
        args.append("-DNEKTAR_USE_FFTW=%s" % hasfeature("+fftw"))
        args.append("-DNEKTAR_USE_HDF5=%s" % hasfeature("+hdf5"))
        args.append("-DNEKTAR_USE_MKL=%s" % hasfeature("^intel-oneapi-mkl"))
        args.append("-DNEKTAR_USE_MPI=%s" % hasfeature("+mpi"))
        args.append("-DNEKTAR_USE_OPENBLAS=%s" % hasfeature("^openblas"))
        args.append("-DNEKTAR_USE_PETSC=OFF")
        args.append("-DNEKTAR_USE_SCOTCH=%s" % hasfeature("+scotch"))
        args.append("-DNEKTAR_USE_THREAD_SAFETY=ON")
        return args

    def install(self, spec, prefix):
        super(Nektar, self).install(spec, prefix)
        if "+python" in spec:
            python = which("python")
            with fs.working_dir(self.build_directory):
                python("setup.py", "install", "--prefix", prefix)

    def setup_run_environment(self, env):
        env.append_path(
            "CMAKE_PREFIX_PATH",
            os.path.join(
                self.spec.prefix, os.path.join("lib64", os.path.join("nektar++", "cmake"))
            ),
        )
        env.append_path(
            "PYTHONPATH", os.path.abspath(os.path.join(self.spec.prefix, "build_tree"))
        )

    def setup_dependent_run_environment(self, env, dependent_spec):
        self.setup_run_environment(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_run_environment(env)

    def add_files_to_view(self, view, merge_map, skip_if_exists=True):
        super(Nektar, self).add_files_to_view(view, merge_map, skip_if_exists)
        path = self.view_destination(view)
        view.link(os.path.join(path, "lib64", "nektar++"), os.path.join(path, "lib", "nektar++"))
