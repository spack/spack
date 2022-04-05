# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Med(AutotoolsPackage):
    """This package is the MED file format that is the SALOME platform standard
    file for meshes and fields and med is based on HDF5 library."""

    # This is a merge of the original 'med' and 'salome-med' packages.
    # NOTE: README.cmake from sources recommends to use autotools build system.

    homepage = "https://docs.salome-platform.org/latest/dev/MEDCoupling/med-file.html"
    url = "https://files.salome-platform.org/Salome/other/med-3.2.0.tar.gz"

    maintainers = ["likask", "franciskloss", "mthcrts"]

    version("4.1.0", sha256="847db5d6fbc9ce6924cb4aea86362812c9a5ef6b9684377e4dd6879627651fce")
    version("4.0.0", sha256="a474e90b5882ce69c5e9f66f6359c53b8b73eb448c5f631fa96e8cd2c14df004")
    version("3.3.1", sha256="856e9c4bb75eb0cceac3d5a5c65b1ce52fb3c46b9182920e1c9f34ae69bd2d5f")
    version("3.2.0", sha256="d52e9a1bdd10f31aa154c34a5799b48d4266dc6b4a5ee05a9ceda525f2c6c138")

    variant("mpi", default=False, description="Enable MPI")
    variant("shared", default=True, description="Build MED-file shared libraries")
    variant("fortran", default=False, description="Enable Fortran")
    variant("int64", default=False, description="Set the default Fortran INTEGER size to 8")
    variant("python", default=False, description="Enables python bindings")
    variant("mesgerr", default=True, description="Enable display of library error messages")
    variant("api23", default=True, description="Enable a complete MED 2.3.6 API")

    depends_on("mpi", when="+mpi")
    depends_on("python", when="+python")
    depends_on("swig", when="+python")

    depends_on("hdf5~mpi", when="~mpi")
    depends_on("hdf5+mpi", when="+mpi")

    depends_on("hdf5@1.10.3", when="@4:")
    depends_on("hdf5@1.8.14", when="@:3.4")

    # C++11 requires a space between literal and identifier
    patch("add_space.patch", when="@3.2.0")
    patch("MAJ_400_410_champs.patch", when="@4.1.0~shared", working_dir="./tools/medimport/4.0.0")

    def check(self):
        with working_dir(self.build_directory):
            make("test", parallel=False)

    def setup_build_environment(self, env):
        spec = self.spec
        env.set("CC", spec["mpi"].mpicc)
        env.set("CXX", spec["mpi"].mpicxx)
        env.set("FC", spec["mpi"].mpifc)
        env.set("F77", spec["mpi"].mpifc)
        env.set("HDF5_ROOT_DIR", spec["hdf5"].prefix)
        if "+fortran" in spec:
            if "+int64" in spec:
                env.append_flags("FFLAGS", "-fdefault-integer-8")
                env.append_flags("FCFLAGS", "-fdefault-integer-8")

    def configure_args(self):
        spec = self.spec
        args = ["--with-hdf5={0}".format(spec["hdf5"].prefix)]

        args += self.with_or_without("mpi")
        args += self.enable_or_disable("shared")
        args += self.enable_or_disable("python")
        args += self.with_or_without("swig", variant="python")
        args += self.enable_or_disable("mesgerr")
        args += self.enable_or_disable("fortran")
        args += self.enable_or_disable("api23")

        if self.run_tests:
            args.extend(["--enable-installtest"])

        return args

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.bin)
        env.prepend_path(
            "PYTHONPATH",
            join_path(
                self.prefix.lib,
                "python{0}".format(self.spec["python"].version.up_to(2)),
                "site-packages",
            ),
        )
