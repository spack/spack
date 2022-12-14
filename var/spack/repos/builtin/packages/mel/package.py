# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------

from spack.package import *

class Mel(MakefilePackage):
    """MPI implementation of Half-approximate Graph Matching"""

    homepage = "https://github.com/ECP-ExaGraph/mel"
    git = "https://github.com/ECP-ExaGraph/mel.git" 

    maintainers = ["Cgbrl28"]

    version("develop",branch="master")

    variant("openmp", default=True, description = "Openmp support")
    variant("opt",default=True, description = "Opt flags")

    depends_on("mpi")

    @property
    def build_targets(self):
        targets = []
        cxxflags = ["-std=c++17 -g"]
        ldflags = [] 

        if "+openmp" in self.spec:
            cxxflags.append(self.compiler.openmp_flag)
            ldflags.append(self.compiler.openmp_flag)
        if "+opt" in self.spec:
            cxxflags.append("-O3")

        targets.append("CXXFLAGS={0}".format(" ".join(cxxflags)))
        targets.append("OPTFLAGS={0}".format(" ".join(ldflags)))
        targets.append("CXX={0}".format(self.spec["mpi"].mpicxx))
        return targets

    def install(self, spec, prefix):

        mkdirp(prefix.bin)
        install("Mel", prefix.bin)
