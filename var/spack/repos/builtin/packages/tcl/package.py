# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from llnl.util.filesystem import find_first

from spack.package import *
from spack.util.environment import is_system_path


class Tcl(AutotoolsPackage, SourceforgePackage):
    """Tcl (Tool Command Language) is a very powerful but easy to learn dynamic
    programming language, suitable for a very wide range of uses, including web and
    desktop applications, networking, administration, testing and many more. Open source
    and business-friendly, Tcl is a mature yet evolving language that is truly cross
    platform, easily deployed and highly extensible."""

    homepage = "https://www.tcl.tk/"
    sourceforge_mirror_path = "tcl/tcl8.6.11-src.tar.gz"

    version("8.6.12", sha256="26c995dd0f167e48b11961d891ee555f680c175f7173ff8cb829f4ebcde4c1a6")
    version("8.6.11", sha256="8c0486668586672c5693d7d95817cb05a18c5ecca2f40e2836b9578064088258")
    version("8.6.10", sha256="5196dbf6638e3df8d5c87b5815c8c2b758496eb6f0e41446596c9a4e638d87ed")
    version("8.6.8", sha256="c43cb0c1518ce42b00e7c8f6eaddd5195c53a98f94adc717234a65cbcfd3f96a")
    version("8.6.6", sha256="a265409781e4b3edcc4ef822533071b34c3dc6790b893963809b9fe221befe07")
    version("8.6.5", sha256="ce26d5b9c7504fc25d2f10ef0b82b14cf117315445b5afa9e673ed331830fb53")
    version("8.6.4", sha256="9e6ed94c981c1d0c5f5fefb8112d06c6bf4d050a7327e95e71d417c416519c8d")
    version("8.6.3", sha256="6ce0778de0d50daaa9c345d7c1fd1288fb658f674028812e7eeee992e3051005")
    version("8.5.19", sha256="d3f04456da873d17f02efc30734b0300fb6c3b85028d445fe284b83253a6db18")

    extendable = True

    depends_on("zlib")

    configure_directory = "unix"

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make("install")

            # https://wiki.tcl-lang.org/page/kitgen
            if self.spec.satisfies("@8.6:"):
                make("install-headers")

            # Some applications like Expect require private Tcl headers.
            make("install-private-headers")

            # Copy source to install tree
            # A user-provided install option might re-do this
            # https://github.com/spack/spack/pull/4102/files
            installed_src = join_path(self.spec.prefix, "share", self.name, "src")
            stage_src = os.path.realpath(self.stage.source_path)
            install_tree(stage_src, installed_src)

            # Replace stage dir -> installed src dir in tclConfig
            filter_file(
                stage_src,
                installed_src,
                join_path(self.spec["tcl"].libs.directories[0], "tclConfig.sh"),
            )

        # Don't install binaries in src/ tree
        with working_dir(join_path(installed_src, self.configure_directory)):
            make("clean")

    @run_after("install")
    def symlink_tclsh(self):
        with working_dir(self.prefix.bin):
            symlink("tclsh{0}".format(self.version.up_to(2)), "tclsh")

    # ========================================================================
    # Set up environment to make install easy for tcl extensions.
    # ========================================================================

    @property
    def libs(self):
        return find_libraries(
            ["libtcl{0}".format(self.version.up_to(2))], root=self.prefix, recursive=True
        )

    @property
    def command(self):
        """Returns the tclsh command.

        Returns:
            Executable: the tclsh command
        """
        # Although we symlink tclshX.Y to tclsh, we also need to support external
        # installations that may not have this symlink, or may have multiple versions
        # of Tcl installed in the same directory.
        return Executable(
            os.path.realpath(self.prefix.bin.join("tclsh{0}".format(self.version.up_to(2))))
        )

    def _find_script_dir(self):
        # Put more-specific prefixes first
        check_prefixes = [
            join_path(self.prefix, "share", "tcl{0}".format(self.version.up_to(2))),
            self.prefix,
        ]
        for prefix in check_prefixes:
            result = find_first(prefix, "init.tcl")
            if result:
                return os.path.dirname(result)
        raise RuntimeError("Cannot locate init.tcl")

    def setup_run_environment(self, env):
        """Set TCL_LIBRARY to the directory containing init.tcl.

        For further info see:

        * https://wiki.tcl-lang.org/page/TCL_LIBRARY
        """
        # When using tkinter from within spack provided python+tkinter,
        # python will not be able to find Tcl unless TCL_LIBRARY is set.
        env.set("TCL_LIBRARY", self._find_script_dir())

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Set TCL_LIBRARY to the directory containing init.tcl.
        Set TCLLIBPATH to include the tcl-shipped directory for
        extensions and any other tcl extension it depends on.

        For further info see:

        * https://wiki.tcl-lang.org/page/TCL_LIBRARY
        * https://wiki.tcl-lang.org/page/TCLLIBPATH
        """
        env.set("TCL_LIBRARY", self._find_script_dir())

        # If we set TCLLIBPATH, we must also ensure that the corresponding
        # tcl is found in the build environment. This to prevent cases
        # where a system provided tcl is run against the standard libraries
        # of a Spack built tcl. See issue #7128 that relates to python but
        # it boils down to the same situation we have here.
        if not is_system_path(self.prefix.bin):
            env.prepend_path("PATH", self.prefix.bin)

        # WARNING: paths in $TCLLIBPATH must be *space* separated,
        # its value is meant to be a Tcl list, *not* an env list
        # as explained here: https://wiki.tcl-lang.org/page/TCLLIBPATH:
        # "TCLLIBPATH is a Tcl list, not some platform-specific
        # colon-separated or semi-colon separated format"

        # WARNING: Tcl and Tcl extensions like Tk install their configuration files
        # in subdirectories like `<prefix>/lib/tcl8.6`. However, Tcl is aware of this,
        # and $TCLLIBPATH should only contain `<prefix>/lib`. $TCLLIBPATH is only needed
        # because we install Tcl extensions to different directories than Tcl. See:
        # https://core.tcl-lang.org/tk/tktview/447bd3e4abe17452d19a80e6840dcc8a2603fcbc
        env.prepend_path("TCLLIBPATH", self.spec["tcl"].libs.directories[0], separator=" ")

        for d in dependent_spec.traverse(deptype=("build", "run", "test")):
            if d.package.extends(self.spec):
                # Tcl libraries may be installed in lib or lib64, see #19546
                for lib in ["lib", "lib64"]:
                    tcllibpath = join_path(d.prefix, lib)
                    if os.path.exists(tcllibpath):
                        env.prepend_path("TCLLIBPATH", tcllibpath, separator=" ")

    def setup_dependent_run_environment(self, env, dependent_spec):
        """Set TCLLIBPATH to include the tcl-shipped directory for
        extensions and any other tcl extension it depends on.

        For further info see:

        * https://wiki.tcl-lang.org/page/TCLLIBPATH
        """
        for d in dependent_spec.traverse(deptype=("build", "run", "test")):
            if d.package.extends(self.spec):
                # Tcl libraries may be installed in lib or lib64, see #19546
                for lib in ["lib", "lib64"]:
                    tcllibpath = join_path(d.prefix, lib)
                    if os.path.exists(tcllibpath):
                        env.prepend_path("TCLLIBPATH", tcllibpath, separator=" ")
