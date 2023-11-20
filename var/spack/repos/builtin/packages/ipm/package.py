# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.util.executable import Executable


class Ipm(AutotoolsPackage):
    """IPM is a portable profiling infrastructure for parallel codes.
    It provides a low-overhead profile of application performance
    and resource utilization in a parallel program. Communication,
    computation, and IO are the primary focus."""

    homepage = "https://github.com/nerscadmin/IPM"
    git = "https://github.com/nerscadmin/IPM.git"

    maintainers("Christoph-TU")

    version("master", branch="master", preferred=True)
    version("2.0.6", tag="2.0.6", commit="b008141ee16d39b33e20bffde615564afa107575")

    variant("papi", default=False, description="Enable PAPI")
    variant("cuda", default=False, description="Enable CUDA")
    variant("libunwind", default=False, description="Enable libunwind")

    variant(
        "papi_multiplexing", default=False, when="+papi", description="Enable PAPI multiplexing"
    )
    variant(
        "coll_details",
        default=False,
        description="Enable detailed monitoring of collective operations (experimental)",
    )
    variant("posixio", default=False, description="Enable POSIXIO")
    variant("pmon", default=False, description="Enable power monitoring module")
    variant("parser", default=False, description="Add dependencies for running ipm_parse")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("mpi")
    depends_on("papi", when="+papi")
    depends_on("cuda", when="+cuda")
    depends_on("libunwind", when="+libunwind")

    # These are required when running the perl script ipm_parse,
    # which is used to create reports from the generated xml file
    depends_on("perl", type="run", when="+parser")
    depends_on("ploticus", type="run", when="+parser")

    # 2COMPLEX and 2DOUBLE_COMPLEX are non-standard types and lead
    # to compile errors when building with coll_details
    patch("remove_MPI_2COMPLEX_and_MPI_2DOUBLE_COMPLEX.patch", when="+coll_details")

    def patch(self):
        filter_file(r"#!/usr/bin/perl", "#!/usr/bin/env perl", "bin/ipm_parse")

    def setup_build_environment(self, env):
        spec = self.spec
        env.set("MPICC", spec["mpi"].mpicc)
        env.set("MPIFC", spec["mpi"].mpifc)
        env.set("MPICXX", spec["mpi"].mpicxx)
        env.set("MPIF77", spec["mpi"].mpif77)

    def autoreconf(self, spec, prefix):
        script = Executable(join_path(self.stage.source_path, "bootstrap.sh"))
        script()

    def configure_args(self):
        args = []
        spec = self.spec
        if "+papi" in spec:
            args.append("--with-papi={0}".format(spec["papi"].prefix))

        if "+cuda" in spec:
            args.append("--with-cudapath={0}".format(spec["cuda"].prefix))

        if "+libunwind" in spec:
            args.append("--with-libunwind={0}".format(spec["libunwind"].prefix))

        if "+papi_multiplexing" in spec:
            args.append("--enable-papi-multiplexing")

        if "+posixio" in spec:
            args.append("--enable-posixio")

        if "+pmon" in spec:
            args.append("--enable-pmon")

        if "+coll_details" in spec:
            args.append("--enable-coll-details")

        args.extend(
            [
                "CFLAGS={0}".format(self.compiler.cc_pic_flag),
                "CXXFLAGS={0}".format(self.compiler.cxx_pic_flag),
            ]
        )
        return args
