# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class TclBwidget(Package):
    """The BWidget Toolkit is a high-level Widget Set for Tcl/Tk
    built using native Tcl/Tk 8.x namespaces."""

    homepage = "https://core.tcl-lang.org/bwidget"
    url      = "https://sourceforge.net/projects/tcllib/files/BWidget/1.9.14/bwidget-1.9.14.tar.gz"

    maintainers = ['fcannini']

    version('1.9.14', sha256='8e9692140167161877601445e7a5b9da5bb738ce8d08ee99b016629bc784a672')

    depends_on('tcl', type=('build', 'run'))
    depends_on('tk', type=('build', 'run'))

    extends('tcl')

    def install(self, spec, prefix):
        pkgdir = join_path(prefix.lib, ''.join(['bwidget', str(self.version)]))

        mkdirp(pkgdir)
        install_tree(self.stage.source_path, pkgdir)
