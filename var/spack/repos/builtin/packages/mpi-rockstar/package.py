# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MpiRockstar(MakefilePackage):
    """MPI-Rockstar: a Hybrid MPI and OpenMP Parallel Implementation of the Rockstar Halo finder"""

    homepage = "https://github.com/Tomoaki-Ishiyama/mpi-rockstar"
    url = "https://github.com/Tomoaki-Ishiyama/mpi-rockstar/archive/42a2080e71de72c4f022f5cd44585929b5f99d66.tar.gz"

    license("GPL-3.0-only", checked_by="lgarrison")

    version(
        "v1.0.0-24-g42a2080",
        sha256="14a15fd94817ba59283d4e8947678d68aa6367c7ccedc3386aaae6187609d7f1",
    )

    variant("hdf5", default=False, description="Enable HDF5 support")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("mpi")
    depends_on("hdf5", when="+hdf5")
    depends_on("libtirpc")

    build_directory = "src"

    def edit(self, spec, prefix):
        makefile = FileFilter(join_path(self.build_directory, "Makefile"))
        makefile.filter(r"-I/usr/include/tirpc", "")
        makefile.filter(r"-std=c\+\+11", "-std=c++14")

    @property
    def build_targets(self):
        targets = ["find_parents"]
        if "+hdf5" in self.spec:
            targets += ["mpi-rockstar_hdf5"]
        else:
            targets += ["mpi-rockstar"]
        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("find_parents", prefix.bin)

        if "+hdf5" in spec:
            install("mpi-rockstar_hdf5", prefix.bin)
        else:
            install("mpi-rockstar", prefix.bin)
