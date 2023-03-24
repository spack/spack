# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class Slepc(Package, CudaPackage, ROCmPackage):
    """Scalable Library for Eigenvalue Problem Computations."""

    homepage = "https://slepc.upv.es"
    url = "https://slepc.upv.es/download/distrib/slepc-3.17.1.tar.gz"
    git = "https://gitlab.com/slepc/slepc.git"

    maintainers("joseeroman", "balay")

    tags = ["e4s"]
    test_requires_compiler = True

    version("main", branch="main")
    version("3.18.2", sha256="5bd90a755934e702ab1fdb3320b9fe75ab5fc28c93d364248ea86a372fbe6a62")
    version("3.18.1", sha256="f6e6e16d8399c3f94d187da9d4bfdfca160de50ebda7d63f6fa8ef417597e9b4")
    version("3.18.0", sha256="18af535d979a646363df01f407c75f0e3b0dd97b3fdeb20dca25b30cd89239ee")
    version("3.17.2", sha256="f784cca83a14156631d6e0f5726ca0778e259e1fe40c927607d5fb12d958d705")
    version("3.17.1", sha256="11386cd3f4c0f9727af3c1c59141cc4bf5f83bdf7c50251de0845e406816f575")
    version("3.17.0", sha256="d4685fed01b2351c66706cbd6d08e4083a4645df398ef5ccd68fdfeb2f86ea97")
    version("3.16.3", sha256="b92bd170632a3de4d779f3f0697e7cb9b663e2c34606c9e97d899d7c1868014e")
    version("3.16.2", sha256="3ba58f5005513ae0ab9f3b27579c82d245a82687886eaaa67cad4cd6ba2ca3a1")
    version("3.16.1", sha256="b1a8ad8db1ad88c60616e661ab48fc235d5a8b6965023cb6d691b9a2cfa94efb")
    version("3.16.0", sha256="be7292b85430e52210eb389c4f434b67164e96d19498585e82d117e850d477f4")
    version("3.15.2", sha256="15fd317c4dd07bb41a994ad4c27271a6675af5f2abe40b82a64a27eaae2e632a")
    version("3.15.1", sha256="9c7c3a45f0d9df51decf357abe090ef05114c38a69b7836386a19a96fb203aea")
    version("3.15.0", sha256="e53783ae13acadce274ea65c67186b5ab12332cf17125a694e21d598aa6b5f00")
    version("3.14.2", sha256="3e54578dda1f4c54d35ac27d02f70a43f6837906cb7604dbcec0e033cfb264c8")
    version("3.14.1", sha256="cc78a15e34d26b3e6dde003d4a30064e595225f6185c1975bbd460cb5edd99c7")
    version("3.14.0", sha256="37f8bb270169d1d3f5d43756ac8929d56204e596bd7a78a7daff707513472e46")
    version("3.13.4", sha256="ddc9d58e1a4413218f4e67ea3b255b330bd389d67f394403a27caedf45afa496")
    version("3.13.3", sha256="23d179c22b4b2f22d29fa0ac0a62f5355a964d3bc245a667e9332347c5aa8f81")
    version("3.13.2", sha256="04cb8306cb5d4d990509710d7f8ae949bdc2c7eb850930b8d0b0b5ca99f6c70d")
    version("3.13.1", sha256="f4a5ede4ebdee5e15153ce31c1421209c7b794bd94be1430018615fb0838b879")
    version("3.13.0", sha256="f1f3c2d13a1a6914e7bf4746d38761e107ea866f50927b639e4ad5918dd1e53b")
    version("3.12.2", sha256="a586ce572a928ed87f04961850992a9b8e741677397cbaa3fb028323eddf4598")
    version("3.12.1", sha256="a1cc2e93a81c9f6b86abd81022c9d64b0dc2161e77fb54b987f963bc292e286d")
    version("3.12.0", sha256="872831d961cf76389fafb7553231ae1a6676555850c98ea0e893c06f596b2e9e")
    version("3.11.2", sha256="cd6a73ac0c9f689c12f2987000a7a28fa7df53fdc069fb59a2bb148699e741dd")
    version("3.11.1", sha256="4816070d4ecfeea6212c6944cee22dc7b4763df1eaf6ab7847cc5ac5132608fb")
    version("3.11.0", sha256="bf29043c311fe2c549a25e2b0835095723a3eebc1dff288a233b32913b5762a2")

    variant("arpack", default=True, description="Enables Arpack wrappers")
    variant("blopex", default=False, description="Enables BLOPEX wrappers")

    # NOTE: make sure PETSc and SLEPc use the same python.
    depends_on("python@2.6:2.8,3.4:", type="build")

    # Cannot mix release and development versions of SLEPc and PETSc:
    depends_on("petsc@main", when="@main")
    depends_on("petsc@3.18.0:3.18", when="@3.18.0:3.18")
    depends_on("petsc@3.17.0:3.17", when="@3.17.0:3.17")
    depends_on("petsc@3.16.0:3.16", when="@3.16.0:3.16")
    depends_on("petsc@3.15.0:3.15", when="@3.15.0:3.15")
    depends_on("petsc@3.14.0:3.14", when="@3.14.0:3.14")
    depends_on("petsc@3.13.0:3.13", when="@3.13.0:3.13")
    depends_on("petsc@3.12.0:3.12", when="@3.12.0:3.12")
    depends_on("petsc@3.11.0:3.11", when="@3.11.0:3.11")
    depends_on("petsc+cuda", when="+cuda")
    depends_on("arpack-ng~mpi", when="+arpack^petsc~mpi~int64")
    depends_on("arpack-ng+mpi", when="+arpack^petsc+mpi~int64")

    for arch in ROCmPackage.amdgpu_targets:
        rocm_dep = "+rocm amdgpu_target={0}".format(arch)
        depends_on("petsc {0}".format(rocm_dep), when=rocm_dep)

    patch("install_name_371.patch", when="@3.7.1")

    # Arpack can not be used with 64bit integers.
    conflicts("+arpack", when="@:3.12 ^petsc+int64")
    conflicts("+blopex", when="^petsc+int64")

    resource(
        name="blopex",
        url="https://slepc.upv.es/download/external/blopex-1.1.2.tar.gz",
        sha256="0081ee4c4242e635a8113b32f655910ada057c59043f29af4b613508a762f3ac",
        destination=join_path("installed-arch-" + sys.platform + "-c-opt", "externalpackages"),
        when="@:3.12+blopex",
    )

    resource(
        name="blopex",
        git="https://github.com/lobpcg/blopex",
        commit="6eba31f0e071f134a6e4be8eccfb8d9d7bdd5ac7",
        destination=join_path("installed-arch-" + sys.platform + "-c-opt", "externalpackages"),
        when="@3.13.0:+blopex",
    )

    def revert_kokkos_nvcc_wrapper(self):
        # revert changes by kokkos-nvcc-wrapper
        if self.spec.satisfies("^kokkos+cuda+wrapper"):
            env["MPICH_CXX"] = env["CXX"]
            env["OMPI_CXX"] = env["CXX"]
            env["MPICXX_CXX"] = env["CXX"]

    def install(self, spec, prefix):
        # set SLEPC_DIR for installation
        # Note that one should set the current (temporary) directory instead
        # its symlink in spack/stage/ !
        os.environ["SLEPC_DIR"] = os.getcwd()

        self.revert_kokkos_nvcc_wrapper()
        if self.spec.satisfies("%cce"):
            filter_file(
                "          flags = l",
                '          flags = l\n        flags += ["-fuse-ld=gold"]',
                "config/package.py",
            )

        options = []
        if "+arpack" in spec:
            if spec.satisfies("@3.15:"):
                options.extend(
                    [
                        "--with-arpack-include=%s" % spec["arpack-ng"].prefix.include,
                        "--with-arpack-lib=%s" % spec["arpack-ng"].libs.joined(),
                    ]
                )
            else:
                if spec.satisfies("@:3.12"):
                    arpackopt = "--with-arpack-flags"
                else:
                    arpackopt = "--with-arpack-lib"
                if "arpack-ng~mpi" in spec:
                    arpacklib = "-larpack"
                else:
                    arpacklib = "-lparpack,-larpack"
                options.extend(
                    [
                        "--with-arpack-dir=%s" % spec["arpack-ng"].prefix,
                        "%s=%s" % (arpackopt, arpacklib),
                    ]
                )

        # It isn't possible to install BLOPEX separately and link to it;
        # BLOPEX has to be downloaded with SLEPc at configure time
        if "+blopex" in spec:
            options.append("--download-blopex")

        python("configure", "--prefix=%s" % prefix, *options)

        make("V=1")
        if self.run_tests:
            make("test", parallel=False)

        make("install", parallel=False)

    def setup_run_environment(self, env):
        # set SLEPC_DIR & PETSC_DIR in the module file
        env.set("SLEPC_DIR", self.prefix)
        env.set("PETSC_DIR", self.spec["petsc"].prefix)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Set up SLEPC_DIR for dependent packages built with SLEPc
        env.set("SLEPC_DIR", self.prefix)

    @property
    def archive_files(self):
        return [
            join_path(self.stage.source_path, "configure.log"),
            join_path(self.stage.source_path, "make.log"),
        ]

    def run_hello_test(self):
        """Run stand alone test: hello"""
        test_dir = self.test_suite.current_test_data_dir

        if not os.path.exists(test_dir):
            print("Skipping slepc test")
            return

        exe = "hello"
        cc_exe = os.environ["CC"]

        self.run_test(
            exe=cc_exe,
            options=[
                "-I{0}".format(self.prefix.include),
                "-L",
                self.prefix.lib,
                "-l",
                "slepc",
                "-L",
                self.spec["petsc"].prefix.lib,
                "-l",
                "petsc",
                "-L",
                self.spec["mpi"].prefix.lib,
                "-l",
                "mpi",
                "-o",
                exe,
                join_path(test_dir, "hello.c"),
            ],
            purpose="test: compile {0} example".format(exe),
            work_dir=test_dir,
        )

        self.run_test(
            exe=exe,
            options=[],
            expected=["Hello world"],
            purpose="test: run {0} example".format(exe),
            work_dir=test_dir,
        )

    def test(self):
        self.run_hello_test()
