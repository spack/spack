# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import subprocess
import sys
from contextlib import contextmanager

from spack import *


class Neuron(CMakePackage):
    """NEURON is a simulation environment for single and networks of neurons.

    NEURON is a simulation environment for modeling individual and networks of
    neurons. NEURON models individual neurons via the use of sections that are
    automatically subdivided into individual compartments, instead of
    requiring the user to manually create compartments. The primary scripting
    language is hoc but a Python interface is also available.
    """

    homepage = "https://www.neuron.yale.edu/"
    url = "http://www.neuron.yale.edu/ftp/neuron/versions/v7.5/nrn-7.5.tar.gz"
    git = "https://github.com/neuronsimulator/nrn"

    # Patch which reverts 81a7a39 for numerical compat
    patch("revert_Import3d_numerical_format.master.patch", when="@7.8.0c:")
    patch("revert_Import3d_numerical_format.patch", when="@7.8.0:7.8.0b")
    # Patch which reverts d9605cb for not hanging on ExperimentalMechComplex
    patch("apply_79a4d2af_load_balance_fix.patch", when="@7.8.0b")
    patch("fix_brew_py_18e97a2d.patch", when="@7.8.0c")
    # Patch for recent CMake versions that don't identify NVHPC as PGI
    patch("patch-v800-cmake-nvhpc.patch", when="@8.0.0%nvhpc^cmake@3.20:")

    version("develop", branch="master")
    version("8.0.2", tag="8.0.2")
    version("8.0.1", tag="8.0.1")
    version("8.0.0", tag="8.0.0")
    version("7.9.0b",  commit="94147e5")
    version("7.9.0a",  commit="fc74b85")
    version("7.8.1",   tag="7.8.1")
    version("7.8.0c",  commit="e529b4f")
    version("7.8.0b",  commit="92a208b")
    version("7.6.8",   tag="7.6.8")
    version("7.6.6",   tag="7.6.6")
    version("2018-10", commit="b3097b7")
    # versions from url, with checksum
    version(
        "7.5",
        sha256="67642216a969fdc844da1bd56643edeed5e9f9ab8c2a3049dcbcbcccba29c336",
    )
    version(
        "7.4",
        sha256="1403ba16b2b329d2376f4bf007d96e6bf2992fa850f137f1068ad5b22b432de6",
    )
    version(
        "7.3",
        sha256="71cff5962966c5cd5d685d90569598a17b4b579d342126b31e2d431128cc8832",
    )
    version(
        "7.2",
        sha256="c777d73a58ff17a073e8ea25f140cb603b8b5f0df3c361388af7175e44d85b0e",
    )

    variant("cmake",      default=True, description="Build NEURON using cmake")
    variant("binary",     default=True, description="Create special as a binary instead of shell script (8.0.x and earlier)")
    conflicts("~binary", when='@8.0.999:')
    variant("coreneuron", default=False, description="Enable CoreNEURON support")
    variant("mod-compatibility",  default=True, description="Enable CoreNEURON compatibility for MOD files")
    variant("cross-compile",  default=False, description="Build for cross-compile environment")
    variant("debug",          default=False, description="Build with flags -g -O0")
    variant("interviews", default=False, description="Enable GUI with INTERVIEWS")
    variant("legacy-fr",  default=True,  description="Use original faraday, R, etc. instead of 2019 nist constants")
    variant("memacs",     default=True,  description="Enable use of memacs")
    variant("mpi",        default=True,  description="Enable MPI parallelism")
    variant("multisend",  default=True,  description="Enable multi-send spike exchange")
    variant("profile",    default=False, description="Enable Tau profiling")
    variant("python",     default=True,  description="Enable python")
    variant(
        "pysetup",
        default=True,
        description="Build Python module with setup.py",
    )
    variant("rx3d",       default=True,  description="Enable cython translated 3-d rxd. Depends on pysetup")
    variant("shared",     default=True,  description="Build shared libraries")
    variant("tests",      default=False, description="Enable unit tests")
    variant("model_tests", default="None", description="Enable detailed model tests included in neuron", multi=True, values=("None", "olfactory", "channel-benchmark", "tqperf-heavy"))
    variant("legacy-unit", default=True,   description="Enable legacy units")

    variant("codechecks", default=False,
            description="Perform additional code checks like "
                        "formatting or static analysis")

    variant("caliper", default=False, description="Add LLNL/Caliper support")

    # Build with `ninja` instead of `make`
    generator = 'Ninja'
    depends_on('ninja', type='build')

    depends_on("autoconf",  type="build", when="~cmake")
    depends_on("automake",  type="build", when="~cmake")
    depends_on("bison",     type="build")
    depends_on("flex",      type="build")
    depends_on("libtool",   type="build", when="~cmake")
    depends_on("pkgconfig", type="build")

    # Readline became incompatible with Mac so we use neuron internal readline.
    # HOWEVER, with the internal version there is a bug which makes
    # Vector.as_numpy() not work!
    depends_on("readline", when=sys.platform != "darwin")

    # Transient dependency
    depends_on("gettext")

    depends_on("mpi",         when="+mpi")
    depends_on("py-mpi4py",   when="+mpi+python+tests")
    depends_on("ncurses",     when="~cross-compile")
    depends_on("python@2.6:", when="+python", type=("build", "link", "run"))
    depends_on("py-pytest",   when="+python+tests")
    # Numpy is required for Vector.as_numpy()
    depends_on("py-numpy",    when="+python", type=("build", "run"))
    depends_on("py-cython",   when="+rx3d", type="build")
    depends_on("tau",         when="+profile")
    depends_on("coreneuron+legacy-unit~caliper", when="+coreneuron+legacy-unit~caliper")
    depends_on("coreneuron~legacy-unit~caliper", when="+coreneuron~legacy-unit~caliper")
    depends_on("coreneuron+legacy-unit+caliper", when="+coreneuron+legacy-unit+caliper")
    depends_on("coreneuron~legacy-unit+caliper", when="+coreneuron~legacy-unit+caliper")
    depends_on("py-pytest-cov", when="+tests@8:")

    conflicts("+cmake",   when="@0:7.8.0b,2018-10")
    conflicts("~shared",  when="+python")
    conflicts("+pysetup", when="~python")
    conflicts("+rx3d",    when="~python")

    # ==============================================
    # ==== CMake build system related functions ====
    # ==============================================
    @when("+cmake")
    def cmake_args(self):
        def cmake_enable_option(spec_requiremement):
            value = "TRUE" if spec_requiremement in self.spec else "FALSE"
            cmake_name = spec_requiremement[1:].upper().replace("-", "_")
            return "-DNRN_ENABLE_" + cmake_name + ":BOOL=" + value
        args = [cmake_enable_option(variant) for variant in ["+interviews",
                                                             "+legacy-fr",
                                                             "+python",
                                                             "+memacs",
                                                             "+rx3d",
                                                             "+coreneuron",
                                                             "+tests"]]
        compilation_flags = []
        if self.spec.variants['model_tests'].value != ("None",):
            args.append('-DNRN_ENABLE_MODEL_TESTS=' + ",".join(
                model for model in self.spec.variants["model_tests"].value))
        if "+mpi" in self.spec:
            args.append("-DNRN_ENABLE_MPI=ON")
            if "~coreneuron" in self.spec:
                args.append("-DNRN_ENABLE_MPI_DYNAMIC=ON")
        else:
            args.append("-DNRN_ENABLE_MPI=OFF")
        if "+python" in self.spec:
            args.append("-DPYTHON_EXECUTABLE:FILEPATH="
                        + self.spec["python"].command.path)
        if "+debug" in self.spec:
            compilation_flags += ['-g', '-O0']
            # Remove default flags (RelWithDebInfo etc.)
            args.append("-DCMAKE_BUILD_TYPE=Custom")
        if "+mod-compatibility" in self.spec:
            args.append("-DNRN_ENABLE_MOD_COMPATIBILITY:BOOL=ON")
        if "+binary" in self.spec and '@:8.0.999' in self.spec:
            args.append("-DNRN_ENABLE_BINARY_SPECIAL=ON")
        if "+legacy-unit" in self.spec:
            args.append('-DNRN_DYNAMIC_UNITS_USE_LEGACY=ON')
        if "+coreneuron" in self.spec:
            args.append('-DCORENEURON_DIR=' + self.spec["coreneuron"].prefix)
        # NVHPC 21.11 and newer detect ABM support and define __ABM__, which
        # breaks Random123 compilation. NEURON inserts a workaround for this in
        # https://github.com/neuronsimulator/nrn/pull/1587.
        if self.spec.satisfies('@:8.0.999%nvhpc@21.11:'):
            compilation_flags.append('-DR123_USE_INTRIN_H=0')
        # Added in https://github.com/neuronsimulator/nrn/pull/1574, this
        # improves ccache performance in CI builds.
        if self.spec.satisfies('@develop'):
            compilation_flags.append('-DNRN_AVOID_ABSOLUTE_PATHS=ON')
        compilation_flags = ' '.join(compilation_flags)
        args.append("-DCMAKE_C_FLAGS=" + compilation_flags)
        args.append("-DCMAKE_CXX_FLAGS=" + compilation_flags)
        if "+caliper" in self.spec:
            args.append('-DNRN_ENABLE_PROFILING=ON')
            args.append('-DNRN_PROFILER=caliper')
        return args

    # Create symlink in share/nrn/lib for the python libraries
    # which is the place that neuron expects the library similarly
    # to autotools installation
    # See : https://github.com/neuronsimulator/nrn/issues/567
    @run_after("install")
    def symlink_python_lib(self):
        if "+cmake+python" in self.spec:
            os.symlink(self.prefix.lib.python,
                       self.prefix.share.nrn.lib.python)

    # ==============================================
    # == Autotools build system related functions ==
    # ==============================================
    @when("~cmake")
    @run_before("build")
    def set_autoconf_options(self):
        self._default_options = ["--without-iv", "--without-x"]
        self._specs_to_options = {
            "+cross-compile": [
                "cross_compiling=yes",
                "--without-readline",
                "--without-memacs",
                "--without-nmodl",
            ],
            "~python": ["--without-nrnpython"],
            "~pysetup": ["--disable-pysetup"],
            "+mpi+multisend": ["--with-multisend"],
            "~rx3d": ["--disable-rx3d"],
            "~mpi": ["--without-paranrn"],
            "+mpi": ["--with-paranrn=dynamic"],
            "~shared": ["--disable-shared"],
            "+binary": ["linux_nrnmech=no"],
        }

    @when("~cmake")
    def get_arch_options(self, spec):
        options = []

        if spec.satisfies('+cross-compile'):
            options.extend(['cross_compiling=yes',
                            '--without-memacs',
                            '--without-nmodl'])

        # on os-x disable building carbon 'click' utility
        if 'darwin' in self.spec.architecture:
            options.append('macdarwin=no')

        return options

    @when("~cmake")
    def get_python_options(self, spec):
        """Determine config options for Python
        """
        options = []

        if spec.satisfies("+python"):
            python_exec = spec["python"].command.path
            py_inc = spec["python"].headers.directories[0]
            py_lib = spec["python"].prefix.lib

            if not os.path.isdir(py_lib):
                py_lib = spec["python"].prefix.lib64

            options.extend(
                [
                    "--with-nrnpython=%s" % python_exec,
                    "PYINCDIR=%s" % py_inc,
                    "PYLIBDIR=%s" % py_lib,
                ]
            )

            # use python dependency if not cross-compiling or on cray system
            if spec.satisfies("~cross-compile") or "cray" in spec.architecture:
                options.append("PYTHON_BLD=%s" % python_exec)

        return options

    @when("~cmake")
    def get_compilation_options(self, spec):
        """ Build options setting compilers and compilation flags,
            using MPIC[XX] and C[XX]FLAGS
        """
        flags = "-O2 -g"

        if "bgq" in spec.architecture:
            flags = "-O3 -qtune=qp -qarch=qp -q64 -qstrict -qnohot -g"

        if spec.satisfies("+debug"):
            flags = "-g -O0"

        if self.spec.satisfies("%pgi"):
            flags += " " + self.compiler.pic_flag

        options = ["CFLAGS=%s" % flags, "CXXFLAGS=%s" % flags]

        if spec.satisfies("+profile"):
            options.extend(
                [
                    "--disable-dependency-tracking",
                    "CC=%s" % "tau_cc",
                    "CXX=%s" % "tau_cxx",
                ]
            )
            if spec.satisfies("+mpi"):
                options.extend(
                    ["MPICC=%s" % "tau_cc", "MPICXX=%s" % "tau_cxx"]
                )
        elif spec.satisfies("+mpi"):
            options.extend(
                [
                    "MPICC=%s" % spec["mpi"].mpicc,
                    "MPICXX=%s" % spec["mpi"].mpicxx,
                ]
            )
        return options

    # Overload CMakePackage cmake function to build
    # Neuron with the legacy Autotools workflow
    @when("~cmake")
    def cmake(self, spec, prefix):
        return

    @when("~cmake")
    def build_nmodl(self, spec, prefix):
        # build components for front-end arch in cross compiling environment
        options = ["--prefix=%s" % prefix, "--with-nmodl-only", "--without-x"]

        if 'cray' in self.spec.architecture:
            flags = '-target-cpu=x86_64 -target-network=none'
            options.extend(['CFLAGS=%s' % flags,
                            'CXXFLAGS=%s' % flags])

        configure = Executable(join_path(self.stage.source_path, "configure"))
        configure(*options)
        make()
        make("install")

    @when("~cmake")
    def build(self, spec, prefix):
        options = ["--prefix=%s" % prefix] + self._default_options

        for specname, spec_opts in self._specs_to_options.items():
            if spec.satisfies(specname):
                options.extend(spec_opts)

        options.extend(self.get_arch_options(spec))
        options.extend(self.get_python_options(spec))
        options.extend(self.get_compilation_options(spec))

        ld_flags = "LDFLAGS="
        if "readline" in spec:
            # Except in Mac we always depend on readline, which is anyway a
            # python dependency
            options.append("--with-readline=" + spec["readline"].prefix)
            ld_flags += " -L{0.prefix.lib} {0.libs.rpath_flags}".format(
                spec["readline"]
            )
        else:
            options.append("--with-readline=no")

        # To support prompt (not cross-compile) use readline + ncurses
        if "ncurses" in spec:
            options.extend(
                [
                    "CURSES_LIBS={0.rpath_flags} {0.ld_flags}".format(
                        spec["ncurses"].libs
                    ),
                    "CURSES_CFLAGS={0}".format(spec["ncurses"].prefix.include),
                ]
            )
            ld_flags += " -L{0.prefix.lib} {0.libs.rpath_flags}".format(
                spec["ncurses"]
            )

        if spec.satisfies("+mpi"):
            ld_flags += " -Wl,-rpath," + self.spec["mpi"].prefix.lib

        options.append(ld_flags)

        build = Executable("./build.sh")
        build()

        with working_dir("build", create=True):
            if spec.satisfies("+cross-compile"):
                self.build_nmodl(spec, prefix)
            srcpath = self.stage.source_path
            configure = Executable(join_path(srcpath, "configure"))
            configure(*options)
            with profiling_wrapper_on():
                make("VERBOSE=1")

    @when("~cmake")
    def install(self, spec, prefix):
        with working_dir("build"):
            with profiling_wrapper_on():
                make("install")

    @when("~cmake")
    def patch(self):
        # aclocal need complete include path (especially on os x)
        pkgconf_inc = "-I %s/share/aclocal/" % (self.spec["pkgconfig"].prefix)
        libtool_inc = "-I %s/share/aclocal/" % (self.spec["libtool"].prefix)
        newpath = "aclocal -I m4 %s %s" % (pkgconf_inc, libtool_inc)
        filter_file(r"aclocal -I m4", r"%s" % newpath, "build.sh")

        # patch hh.mod to be compatible with coreneuron
        if self.spec.satisfies("+coreneuron"):
            filter_file(r"GLOBAL minf", r"RANGE minf", "src/nrnoc/hh.mod")
            filter_file(r"TABLE minf", r":TABLE minf", "src/nrnoc/hh.mod")

    # ==============================================
    # ============== Common functions ==============
    # ==============================================
    @property
    def archdir(self):
        """Determine the architecture neuron build architecture.

        With cmake get the architecture of the system from spack.
        With autotools instead of recreating the logic of the
        neuron"s configure we dynamically find the architecture-
        specific directory by looking for a specific binary.
        """
        return subprocess.Popen(
            ['awk', '-F=', '$1 == "MODSUBDIR" { print $2; exit; }',
             str(self.prefix.bin.nrnivmodl)],
            stdout=subprocess.PIPE
        ).communicate()[0].decode().strip()

    @property
    def basedir(self):
        """Determine the neuron base directory.

        NEURON base directory is based on the build system. For
        cmake the bin and lib folders are in self.prefix and for
        autotools it is in self.prefix/neuron_arch.
        """
        if self.spec.satisfies("+cmake"):
            neuron_basedir = self.prefix
        else:
            file_list = find(self.prefix, "*/bin/nrniv_makefile")
            # check needed as when initially evaluated the prefix is empty
            if file_list:
                neuron_basedir = os.path.dirname(os.path.dirname(file_list[0]))
            else:
                neuron_basedir = self.prefix
        return neuron_basedir

    @run_after("install")
    def filter_compilers(self):
        """run after install to avoid spack compiler wrappers
        getting embded into nrnivmodl script"""

        cc_compiler = self.compiler.cc
        cxx_compiler = self.compiler.cxx
        if self.spec.satisfies("+mpi"):
            cc_compiler = self.spec["mpi"].mpicc
            cxx_compiler = self.spec["mpi"].mpicxx

        libtool_makefile = join_path(self.prefix,
                                     "share/nrn/libtool")
        nrniv_makefile = join_path(self.prefix,
                                   self.basedir,
                                   "./bin/nrniv_makefile")
        nrnmech_makefile = join_path(self.prefix,
                                     self.basedir,
                                     "./bin/nrnmech_makefile")

        kwargs = {"backup": False, "string": True}

        if self.spec.satisfies("~cmake"):
            # hpe-mpi requires linking to libmpi++
            # and hence needs to use cxx wrapper
            if self.spec.satisfies("+mpi"):
                filter_file(env["CC"],
                            cxx_compiler,
                            libtool_makefile,
                            **kwargs)
            else:
                filter_file(env["CC"],
                            cc_compiler,
                            libtool_makefile,
                            **kwargs)
            filter_file(env["CXX"], cxx_compiler, libtool_makefile, **kwargs)
            # In Cray systems we overwrite the spack compiler with CC or CXX
            # accordingly
            if "cray" in self.spec.architecture:
                filter_file(env["CC"], "cc", libtool_makefile, **kwargs)
                filter_file(env["CXX"], "CC", libtool_makefile, **kwargs)

        # The assign_operator should follow any changes done in
        # "bin/nrnivmodl_makefile_cmake.in" and "bin/nrnmech_makefile.in"
        # when assigning CC and CXX variables
        if self.spec.satisfies("+cmake") and self.spec.satisfies("@:7.99"):
            assign_operator = "?="
        else:
            assign_operator = "="

        filter_file("CC {0} {1}".format(assign_operator, env["CC"]),
                    "CC = {0}".format(cc_compiler),
                    nrnmech_makefile,
                    **kwargs)
        filter_file("CXX {0} {1}".format(assign_operator, env["CXX"]),
                    "CXX = {0}".format(cxx_compiler),
                    nrnmech_makefile,
                    **kwargs)

        if self.spec.satisfies("~cmake"):
            filter_file(env["CC"], cc_compiler, nrniv_makefile, **kwargs)
            filter_file(env["CXX"], cxx_compiler, nrniv_makefile, **kwargs)

    # Added because the bin and lib directories are inside x86_64 dir in the
    # installation directory of autotools installation
    @when("~cmake")
    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("PATH", join_path(self.basedir, "bin"))
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.basedir, "lib"))

    def setup_run_environment(self, env):
        env.prepend_path("PATH", join_path(self.basedir, "bin"))
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.basedir, "lib"))
        if self.spec.satisfies("+mpi"):
            env.set("MPICC_CC", self.compiler.cc)
            env.set("MPICXX_CXX", self.compiler.cxx)
        if self.spec.satisfies("+python"):
            env.prepend_path("PYTHONPATH", self.spec.prefix.lib.python)

    def setup_dependent_package(self, module, dependent_spec):
        dependent_spec.package.neuron_basedir = self.basedir
        dependent_spec.package.nrnivmodl_outdir = self.archdir


@contextmanager
def profiling_wrapper_on():
    os.environ["USE_PROFILER_WRAPPER"] = "1"
    yield
    del os.environ["USE_PROFILER_WRAPPER"]
