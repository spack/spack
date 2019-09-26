# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Tk(AutotoolsPackage):
    """Tk is a graphical user interface toolkit that takes developing
       desktop applications to a higher level than conventional
       approaches. Tk is the standard GUI not only for Tcl, but for
       many other dynamic languages, and can produce rich, native
       applications that run unchanged across Windows, Mac OS X, Linux
       and more."""
    homepage = "http://www.tcl.tk"
    url      = "http://prdownloads.sourceforge.net/tcl/tk8.6.5-src.tar.gz"

    version('8.6.8', '5e0faecba458ee1386078fb228d008ba')
    version('8.6.6', 'dd7dbb3a6523c42d05f6ab6e86096e99')
    version('8.6.5', '11dbbd425c3e0201f20d6a51482ce6c4')
    version('8.6.3', '85ca4dbf4dcc19777fd456f6ee5d0221')
    version('8.5.19', 'e89df710447cce0fc0bde65667c12f85')

    variant('xft', default=True,
            description='Enable X FreeType')
    variant('xss', default=True,
            description='Enable X Screen Saver')

    extends('tcl')

    depends_on('tcl@8.6:', when='@8.6:')
    depends_on('libx11')
    depends_on('libxft', when='+xft')
    depends_on('libxscrnsaver', when='+xss')

    configure_directory = 'unix'

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make('install')

            # Some applications like Expect require private Tk headers.
            make('install-private-headers')

            # Copy source to install tree
            installed_src = join_path(
                self.spec.prefix, 'share', self.name, 'src')
            stage_src = os.path.realpath(self.stage.source_path)
            install_tree(stage_src, installed_src)

            # Replace stage dir -> installed src dir in tkConfig
            filter_file(
                stage_src, installed_src,
                join_path(self.spec.prefix, 'lib', 'tkConfig.sh'))

    @property
    def libs(self):
        return find_libraries(['libtk{0}'.format(self.version.up_to(2))],
                              root=self.prefix, recursive=True)

    def setup_environment(self, spack_env, run_env):
        # When using Tkinter from within spack provided python+tkinter, python
        # will not be able to find Tcl/Tk unless TK_LIBRARY is set.
        run_env.set('TK_LIBRARY', join_path(self.prefix.lib, 'tk{0}'.format(
            self.spec.version.up_to(2))))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('TK_LIBRARY', join_path(self.prefix.lib, 'tk{0}'.format(
            self.spec.version.up_to(2))))

    def configure_args(self):
        spec = self.spec
        config_args = [
            '--with-tcl={0}'.format(spec['tcl'].prefix.lib),
            '--x-includes={0}'.format(spec['libx11'].prefix.include),
            '--x-libraries={0}'.format(spec['libx11'].prefix.lib)
        ]
        config_args += self.enable_or_disable('xft')
        config_args += self.enable_or_disable('xss')

        return config_args

    @run_after('install')
    def symlink_wish(self):
        with working_dir(self.prefix.bin):
            symlink('wish{0}'.format(self.version.up_to(2)), 'wish')
