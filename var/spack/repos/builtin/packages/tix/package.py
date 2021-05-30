# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Tix(AutotoolsPackage):
    """Tix, the Tk Interface eXtension, is a powerful set of user interface components
    that expands the capabilities of your Tcl/Tk and Python applications. Using Tix
    together with Tk will greatly enhance the appearance and functionality of your
    application."""

    homepage = "https://sourceforge.net/projects/tix/"
    url      = "https://sourceforge.net/projects/tix/files/tix/8.4.3/Tix8.4.3-src.tar.gz/download"

    version('8.4.3', sha256='562f040ff7657e10b5cffc2c41935f1a53c6402eb3d5f3189113d734fd6c03cb')

    extends('tcl')
    depends_on('tk')

    patch('https://raw.githubusercontent.com/macports/macports-ports/master/x11/tix/files/panic.patch',
          sha256='1be1a1c7453f6ab8771f90d7e7c0f8959490104752a16a8755bbb7287a841a96',
          level=0)
    patch('https://raw.githubusercontent.com/macports/macports-ports/master/x11/tix/files/patch-generic-tixGrSort.c.diff',
          sha256='99b33cc307f71bcf9cc6f5a44b588f22956884ce3f1e4c716ad64c79cf9c5f41',
          level=0)
    patch('https://raw.githubusercontent.com/macports/macports-ports/master/x11/tix/files/implicit.patch',
          sha256='8a2720368c7757896814684147029d8318b9aa3b0914b3f37dd5e8a8603a61d3',
          level=0)

    def configure_args(self):
        spec = self.spec
        args = [
            '--with-tcl={0}'.format(spec['tcl'].libs.directories[0]),
            '--with-tk={0}'.format(spec['tk'].libs.directories[0]),
            '--exec-prefix={0}'.format(self.prefix),
        ]
        return args

    @property
    def libs(self):
        return find_libraries(['libTix{0}'.format(self.version)],
                              root=self.prefix, recursive=True)

    def setup_run_environment(self, env):
        """Set TIX_LIBRARY to the directory containing Tix.tcl.

        For further info, see:

        * http://tix.sourceforge.net/docs/pdf/TixUser.pdf
        """
        # When using tkinter.tix from within spack provided python+tkinter+tix,
        # python will not be able to find Tix unless TIX_LIBRARY is set.
        env.set('TIX_LIBRARY', os.path.dirname(find(self.prefix, 'Tix.tcl')[0]))

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Set TIX_LIBRARY to the directory containing Tix.tcl.

        For further info, see:

        * http://tix.sourceforge.net/docs/pdf/TixUser.pdf
        """
        env.set('TIX_LIBRARY', os.path.dirname(find(self.prefix, 'Tix.tcl')[0]))
