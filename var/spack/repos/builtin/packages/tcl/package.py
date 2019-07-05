# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.util.environment import is_system_path
from spack import *


class Tcl(AutotoolsPackage):
    """Tcl (Tool Command Language) is a very powerful but easy to
       learn dynamic programming language, suitable for a very wide
       range of uses, including web and desktop applications,
       networking, administration, testing and many more. Open source
       and business-friendly, Tcl is a mature yet evolving language
       that is truly cross platform, easily deployed and highly
       extensible."""
    homepage = "http://www.tcl.tk"
    url      = "http://prdownloads.sourceforge.net/tcl/tcl8.6.5-src.tar.gz"

    version('8.6.8', '81656d3367af032e0ae6157eff134f89')
    version('8.6.6', '5193aea8107839a79df8ac709552ecb7')
    version('8.6.5', '0e6426a4ca9401825fbc6ecf3d89a326')
    version('8.6.4', 'd7cbb91f1ded1919370a30edd1534304')
    version('8.6.3', 'db382feca91754b7f93da16dc4cdad1f')
    version('8.5.19', '4f4e1c919f6a6dbb37e9a12d429769a6')

    extendable = True

    depends_on('zlib')

    configure_directory = 'unix'

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make('install')

            # http://wiki.tcl.tk/17463
            if self.spec.satisfies('@8.6:'):
                make('install-headers')

            # Some applications like Expect require private Tcl headers.
            make('install-private-headers')

            # Copy source to install tree
            # A user-provided install option might re-do this
            # https://github.com/spack/spack/pull/4102/files
            installed_src = join_path(
                self.spec.prefix, 'share', self.name, 'src')
            stage_src = os.path.realpath(self.stage.source_path)
            install_tree(stage_src, installed_src)

            # Replace stage dir -> installed src dir in tclConfig
            filter_file(
                stage_src, installed_src,
                join_path(self.spec.prefix, 'lib', 'tclConfig.sh'))

        # Don't install binaries in src/ tree
        with working_dir(join_path(installed_src, self.configure_directory)):
            make('clean')

    @run_after('install')
    def symlink_tclsh(self):
        with working_dir(self.prefix.bin):
            symlink('tclsh{0}'.format(self.version.up_to(2)), 'tclsh')

    # ========================================================================
    # Set up environment to make install easy for tcl extensions.
    # ========================================================================

    @property
    def libs(self):
        return find_libraries(['libtcl{0}'.format(self.version.up_to(2))],
                              root=self.prefix, recursive=True)

    @property
    def command(self):
        """Returns the tclsh command.

        :returns: The tclsh command
        :rtype: Executable
        """
        return Executable(os.path.realpath(self.prefix.bin.tclsh))

    @property
    def tcl_lib_dir(self):
        """The Tcl version-specific library directory where all extensions are
        installed."""
        return 'lib'

    @property
    def tcl_builtin_lib_dir(self):
        """The Tcl version-specific library directory where all builtin
        extensions are installed."""
        return join_path(self.tcl_lib_dir,
                         'tcl{0}'.format(self.version.up_to(2)))

    def setup_environment(self, spack_env, run_env):
        # When using Tkinter from within spack provided python+tkinter, python
        # will not be able to find Tcl/Tk unless TCL_LIBRARY is set.
        run_env.set('TCL_LIBRARY', join_path(self.prefix, self.tcl_lib_dir))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        """Set TCLLIBPATH to include the tcl-shipped directory for
        extensions and any other tcl extension it depends on.
        For further info see: https://wiki.tcl.tk/1787"""

        spack_env.set('TCL_LIBRARY', join_path(self.prefix, self.tcl_lib_dir))

        # If we set TCLLIBPATH, we must also ensure that the corresponding
        # tcl is found in the build environment. This to prevent cases
        # where a system provided tcl is run against the standard libraries
        # of a Spack built tcl. See issue #7128 that relates to python but
        # it boils down to the same situation we have here.
        path = os.path.dirname(self.command.path)
        if not is_system_path(path):
            spack_env.prepend_path('PATH', path)

        tcl_paths = [join_path(self.prefix, self.tcl_builtin_lib_dir)]

        for d in dependent_spec.traverse(deptype=('build', 'run', 'test')):
            if d.package.extends(self.spec):
                tcl_paths.append(join_path(d.prefix, self.tcl_lib_dir))

        # WARNING: paths in $TCLLIBPATH must be *space* separated,
        # its value is meant to be a Tcl list, *not* an env list
        # as explained here: https://wiki.tcl.tk/1787:
        # "TCLLIBPATH is a Tcl list, not some platform-specific
        # colon-separated or semi-colon separated format"
        tcllibpath = ' '.join(tcl_paths)
        spack_env.set('TCLLIBPATH', tcllibpath)

        # For run time environment set only the path for
        # dependent_spec and prepend it to TCLLIBPATH
        if dependent_spec.package.extends(self.spec):
            dependent_tcllibpath = join_path(dependent_spec.prefix,
                                             self.tcl_lib_dir)
            run_env.prepend_path('TCLLIBPATH', dependent_tcllibpath,
                                 separator=' ')
