# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


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

    extends('tcl')

    depends_on('tcl@8.6:')
    depends_on('libx11')

    configure_directory = 'unix'

    @property
    def libs(self):
        return LibraryList([])

    def setup_environment(self, spack_env, run_env):
        # When using Tkinter from within spack provided python+tk, python
        # will not be able to find Tcl/Tk unless TK_LIBRARY is set.
        run_env.set('TK_LIBRARY', join_path(self.prefix.lib, 'tk{0}'.format(
            self.spec.version.up_to(2))))

    def configure_args(self):
        spec = self.spec
        return ['--with-tcl={0}'.format(spec['tcl'].prefix.lib)]

    @run_after('install')
    def symlink_wish(self):
        with working_dir(self.prefix.bin):
            symlink('wish{0}'.format(self.version.up_to(2)), 'wish')
