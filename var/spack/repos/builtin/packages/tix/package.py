# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tix(AutotoolsPackage):
    """Tix is a powerful high-level widget set that expands the capabilities
       of your Tk/Tcl and Python applications."""

    homepage = "https://sourceforge.net/projects/tix/"
    url      = "https://sourceforge.net/projects/tix/files/tix/8.4.3/Tix8.4.3-src.tar.gz/download"
    version('8.4.3', '2b8bf4b10a852264678182652f477e59')

    extends('tcl')
    depends_on('tk@:8.5.99')
    depends_on('tcl@:8.5.99')

    def configure_args(self):
        spec = self.spec
        config_args = ['--with-tcl={0}'.format(spec['tcl'].prefix.lib),
                       '--with-tk={0}'.format(spec['tk'].prefix.lib),
                       '--exec-prefix={0}'.format(spec.prefix)]
        return config_args

    def install(self, spec, prefix):
        make('install')
        with working_dir(self.prefix.lib):
            symlink('Tix{0}/libTix{0}.{1}'.format(self.version, dso_suffix),
                    'libtix.{0}'.format(dso_suffix))
