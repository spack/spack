# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class Neuron(CMakePackage):
    """NEURON is a simulation environment for single and networks of neurons.
    NEURON is a simulation environment for modeling individual and networks of
    neurons. NEURON models individual neurons via the use of sections that are
    automatically subdivided into individual compartments, instead of
    requiring the user to manually create compartments.
    """

    homepage = "https://www.neuron.yale.edu/"
    url      = "https://neuron.yale.edu/ftp/neuron/versions/v7.7/nrn-7.7.tar.gz"
    git      = "https://github.com/neuronsimulator/nrn"
    maintainers = ['pramodk', 'nrnhines', 'iomaganaris', 'alexsavulescu']

    version('develop', branch='master')
    version("7.8.2", tag="7.8.2")
    version('7.7', sha256='85a0f999a9cdcc661b0066c32a78239e252f26e74eee5328bf1106393400bfc0')
    version('7.6', sha256='5a6133bfa818ec3278fc8d0ecd312674805ae42854f71552f8cd47d98ff6ad2d')
    version('7.5', sha256='67642216a969fdc844da1bd56643edeed5e9f9ab8c2a3049dcbcbcccba29c336')
    version('7.4', sha256='1403ba16b2b329d2376f4bf007d96e6bf2992fa850f137f1068ad5b22b432de6')
    version('7.3', sha256='71cff5962966c5cd5d685d90569598a17b4b579d342126b31e2d431128cc8832')
    version('7.2', sha256='c777d73a58ff17a073e8ea25f140cb603b8b5f0df3c361388af7175e44d85b0e')

    variant("cmake",         default=True, description="Build using cmake build system")
    variant("coreneuron",    default=False, description="Enable CoreNEURON as submodule")
    variant("cross-compile", default=False, description="Build for cross-compile environment")
    variant("interviews",    default=False, description="Enable GUI with INTERVIEWS")
    variant("legacy-unit",   default=False, description="Enable legacy units")
    variant("gpu",           default=False, description="Enable GPU support via CoreNEURON")
    variant("mpi",           default=True,  description="Enable MPI parallelism")
    variant("python",        default=True,  description="Enable python")
    variant("rx3d",          default=False,  description="Enable cython translated 3-d rxd")
    variant("tests",         default=False, description="Enable unit tests")

    depends_on("autoconf",  type="build", when="~cmake")
    depends_on("automake",  type="build", when="~cmake")
    depends_on("bison",     type="build", when="+cmake")
    depends_on("flex",      type="build", when="+cmake")
    depends_on("libtool",   type="build", when="~cmake")
    depends_on("pkgconfig", type="build", when="~cmake")
    depends_on("py-cython", when="+rx3d", type="build")

    depends_on("cuda@8:",     when="+gpu")
    depends_on("gettext")
    depends_on("mpi",         when="+mpi")
    depends_on("ncurses")
    depends_on("python@2.7:", when="+python")
    depends_on("py-pytest",   when="+python+tests")
    depends_on("readline")

    conflicts("+cmake",       when="@0:7.8.0")
    conflicts("+coreneuron",  when="~cmake")
    conflicts("+gpu",         when="@:7.99")
    conflicts("+gpu",         when="~coreneuron")
    conflicts("+interviews",  when="~cmake")
    conflicts("+rx3d",        when="~python")

    patch("patch-v782-git-cmake.patch", when="@7.8.2+cmake")

    # ==============================================
    # ==== CMake build system related functions ====
    # ==============================================

    @when("+cmake")
    def cmake_args(self):
        spec = self.spec
        def cmake_enable_option(spec_options):
            value = "TRUE" if spec_options in spec else "FALSE"
            cmake_name = spec_options[1:].upper().replace("-", "_")
            return "-DNRN_ENABLE_" + cmake_name + ":BOOL=" + value

        args = [cmake_enable_option(variant) for variant in ["+coreneuron",
                                                             "+interviews",
                                                             "+mpi",
                                                             "+python",
                                                             "+rx3d",
                                                             "+coreneuron",
                                                             "+tests"]]
        args.append("-DNRN_ENABLE_BINARY_SPECIAL=ON")

        if "+gpu" in spec:
            args.append("-DCORENRN_ENABLE_GPU=ON")

        if "+mpi" in spec:
            args.append("-DNRN_ENABLE_MPI_DYNAMIC=ON")

        if "+python" in spec:
            args.append("-DPYTHON_EXECUTABLE:FILEPATH="
                        + spec["python"].command.path)

        if spec.variants['build_type'].value == 'Debug':
            args.append("-DCMAKE_C_FLAGS=-g -O0")
            args.append("-DCMAKE_CXX_FLAGS=-g -O0")
            args.append("-DCMAKE_BUILD_TYPE=Custom")

        if "+legacy-unit" in spec:
            args.append('-DNRN_DYNAMIC_UNITS_USE_LEGACY=ON')

        return args


    # ==============================================
    # == Autotools build system related functions ==
    # ==============================================

    # overload cmake phase for legacy Autotools build
    @when("~cmake")
    def cmake(self, spec, prefix):
        return

    # build nmodl separately (in cross compiling environment)
    def build_nmodl(self, spec, prefix):
        options = ["--prefix=%s" % prefix, "--with-nmodl-only", "--without-x"]
        if "cray" in spec.architecture:
            flags = "-target-cpu=x86_64 -target-network=none"
            options.extend(["CFLAGS=%s" % flags, "CXXFLAGS=%s" % flags])

        configure = Executable(join_path(self.stage.source_path, "configure"))
        configure(*options)
        make()
        make("install")

    @when("~cmake")
    def build(self, spec, prefix):
        # default options
        options = ["--prefix=%s" % prefix,
                   "--without-iv",
                   "--without-x"]

        # build options based on variants
        specs_to_options = {
            "+cross-compile": [
                "cross_compiling=yes",
                "--without-readline",
                "--without-memacs",
                "--without-nmodl",
            ],
            "~python": ["--without-nrnpython"],
            "~readline": ["-with-readline=no"],
            "~rx3d": ["--disable-rx3d"],
            "~mpi": ["--without-paranrn"],
            "+mpi": ["--with-paranrn=dynamic"],
        }

        for specname, spec_opts in specs_to_options.items():
            if spec.satisfies(specname):
                options.extend(spec_opts)

        if "darwin" in spec.architecture:
            options.append("macdarwin=no")

        # python build options
        if spec.satisfies("+python"):
            python_exec = spec["python"].command.path
            py_inc = spec["python"].headers.directories[0]
            py_lib = spec["python"].prefix.lib

            if not os.path.isdir(py_lib):
                py_lib = spec["python"].prefix.lib64

            options.append("--with-nrnpython=%s" % python_exec)
            options.append("PYINCDIR=%s" % py_inc)
            options.append("PYLIBDIR=%s" % py_lib)

            # use python dependency if not cross-compiling or on cray system
            if spec.satisfies("~cross-compile") or "cray" in spec.architecture:
                options.append("PYTHON_BLD=%s" % python_exec)

        if spec.variants['build_type'].value == 'Debug':
            flags = "-O0 -g"
        else:
            flags = "-O2 -g"

        if spec.satisfies("%pgi"):
            flags += " " + self.compiler.pic_flag

        options.extend(["CFLAGS=%s" % flags, "CXXFLAGS=%s" % flags])

        if spec.satisfies("+mpi"):
            options.append("MPICC=%s" % spec["mpi"].mpicc)
            options.append("MPICXX=%s" % spec["mpi"].mpicxx)


        ld_flags = "LDFLAGS="

        if "readline" in spec:
            options.append("--with-readline=" + spec["readline"].prefix)
            ld_flags += " -L{0.prefix.lib} -Wl,-rpath,{0.prefix.lib}".format(
                spec["readline"]
            )

        if "ncurses" in spec:
            options.extend(
                [
                    "CURSES_LIBS={0.libs.ld_flags} -Wl,-rpath,{0.prefix.lib}".format(
                        spec["ncurses"]
                    ),
                    "CURSES_CFLAGS={0}".format(spec["ncurses"].prefix.include),
                ]
            )
            ld_flags += " {0.libs.ld_flags} -Wl,-rpath,{0.prefix.lib}".format(
                spec["ncurses"]
            )

        if spec.satisfies("+mpi"):
            ld_flags += " -Wl,-rpath," + spec["mpi"].prefix.lib

        options.append(ld_flags)

        build = Executable("./build.sh")
        build()

        with working_dir("build", create=True):
            if spec.satisfies("+cross-compile"):
                self.build_nmodl(spec, prefix)
            srcpath = self.stage.source_path
            configure = Executable(join_path(srcpath, "configure"))
            configure(*options)
            make()

    @when("~cmake")
    def install(self, spec, prefix):
        with working_dir("build"):
            make("install")

    # ==============================================
    # ============== Common functions ==============
    # ==============================================

    @property
    def basedir(self):
        """Determine the neuron base directory.
        NEURON base directory is based on the build system. For
        cmake the bin and lib folders are in self.prefix and for
        autotools it is in self.prefix/<arch>.
        """
        neuron_basedir = self.prefix
        if self.spec.satisfies("~cmake"):
            file_list = find(self.prefix, "*/bin/nrniv_makefile")
            # check needed as during first evaluation the prefix is empty
            if file_list:
                neuron_basedir = os.path.dirname(os.path.dirname(file_list[0]))

        return neuron_basedir

    @run_after("install")
    def filter_compilers(self):
        """run after install to avoid spack compiler wrappers
        getting embded into nrnivmodl script"""

        spec = self.spec

        if "cray" in spec.architecture:
            cc_compiler = "cc"
            cxx_compiler = "CC"
        elif spec.satisfies("+mpi"):
            cc_compiler = spec["mpi"].mpicc
            cxx_compiler = spec["mpi"].mpicxx
        else:
            cc_compiler = self.compiler.cc
            cxx_compiler = self.compiler.cxx


        kwargs = {"backup": False, "string": True}
        nrnmech_makefile = join_path(self.prefix,
                                     self.basedir,
                                     "./bin/nrnmech_makefile")

        # nrnmech_makefile exists in cmake and autotools but with different syntax
        assign_operator = "?=" if spec.satisfies("+cmake") else "="
        filter_file("CC {0} {1}".format(assign_operator, env["CC"]),
                    "CC = {0}".format(cc_compiler),
                    nrnmech_makefile,
                    **kwargs)
        filter_file("CXX {0} {1}".format(assign_operator, env["CXX"]),
                    "CXX = {0}".format(cxx_compiler),
                    nrnmech_makefile,
                    **kwargs)

        if spec.satisfies("~cmake"):
            nrniv_makefile = join_path(self.prefix,
                                       self.basedir,
                                       "./bin/nrniv_makefile")
            libtool_makefile = join_path(self.prefix, "share/nrn/libtool")
            filter_file(env["CC"], cc_compiler, nrniv_makefile, **kwargs)
            filter_file(env["CXX"], cxx_compiler, nrniv_makefile, **kwargs)
            filter_file(env["CC"], cc_compiler, libtool_makefile, **kwargs)
            filter_file(env["CXX"], cxx_compiler, libtool_makefile, **kwargs)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", join_path(self.basedir, "bin"))
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.basedir, "lib"))
        if self.spec.satisfies("+python"):
            env.prepend_path("PYTHONPATH", self.spec.prefix.lib.python)
