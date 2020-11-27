# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Togl(AutotoolsPackage):
    """ A Tcl/Tk widget for OpenGL rendering."""

    homepage = "https://sourceforge.net/projects/togl"
    url      = homepage + "/files/Togl/2.0/Togl2.0-src.tar.gz"

    version('2.0', sha256='b7d4a90bbad3aca618d505ee99e7fd8fb04c829f63231dda2360f557ba3f7610')

    variant('python', default=False, description='Enable python support')

    depends_on('libxmu')
    depends_on('mesa')
    depends_on('mesa-glu')
    depends_on('tcl', type=('build', 'link', 'run'))
    depends_on('tk', type=('build', 'link', 'run'))
    depends_on('python +tkinter', when='+python', type='run')

    extends('tcl')
    extends('python', when='+python')

    def configure_args(self):
        spec = self.spec

        args = [
            '--libdir={0}'.format(self.prefix.lib),
            '--with-tcl={0}'.format(spec['tcl'].prefix.lib),
            '--with-tk={0}'.format(spec['tk'].prefix.lib),
            '--x-includes={0}'.format(spec['libxmu'].prefix.include)
        ]

        return args

    def install(self, spec, prefix):
        spec = self.spec
        prefix = spec.prefix

        make('install')

        # It seems to be the norm for TCL/TK libraries to not install
        # a 'libwhatever.so' file, not even a symlink
        libtogl = 'libTogl{0}.so'.format(self.version)
        with working_dir(prefix.lib):
            os.symlink(join_path('Togl{0}'.format(self.version), libtogl),
                       libtogl)

        # Empty directory
        pl_lib = join_path(prefix.lib, 'perl5')
        if can_access(pl_lib):
            remove_linked_tree(pl_lib)

        if '+python' in spec:
            py_ver = spec['python'].version.up_to(2)
            py_lib = join_path(prefix.lib, 'python{0}'.format(py_ver))
            py_site = join_path(prefix,
                                spec['python'].package.site_packages_dir)

            install('toglpy.h', prefix.include)
            install('Togl.py', py_site)

        else:
            if can_access(py_lib):
                remove_linked_tree(py_lib)
