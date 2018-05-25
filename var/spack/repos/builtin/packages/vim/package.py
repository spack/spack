##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Vim(AutotoolsPackage):
    """Vim is a highly configurable text editor built to enable efficient text
    editing. It is an improved version of the vi editor distributed with most
    UNIX systems.  Vim is often called a "programmer's editor," and so useful
    for programming that many consider it an entire IDE. It's not just for
    programmers, though. Vim is perfect for all kinds of text editing, from
    composing email to editing configuration files.
    """

    homepage = "http://www.vim.org"
    url      = "https://github.com/vim/vim/archive/v8.0.1376.tar.gz"

    version('8.1.0001', 'edb6f5c67cb3100ea9e3966a43b9c9da')
    version('8.0.1376', '62855881a2d96d48956859d74cfb8a3b')
    version('8.0.0503', '82b77bd5cb38b70514bed47cfe033b8c')
    version('8.0.0454', '4030bf677bdfbd14efb588e4d9a24128')
    version('8.0.0134', 'c74668d25c2acc85d655430dd60886cd')
    version('7.4.2367', 'a0a7bc394f7ab1d95571fe6ab05da3ea')

    feature_sets = ('huge', 'big', 'normal', 'small', 'tiny')
    for fs in feature_sets:
        variant(fs, default=False, description="Use '%s' feature set" % fs)

    variant('python', default=False, description="build with Python")
    depends_on('python', when='+python')

    variant('ruby', default=False, description="build with Ruby")
    depends_on('ruby', when='+ruby')

    variant('lua', default=False, description="build with Lua")
    depends_on('lua', when='+lua')

    variant('perl', default=False, description="build with Perl")
    depends_on('perl', when='+perl')

    variant('cscope', default=False, description="build with cscope support")
    depends_on('cscope', when='+cscope', type='run')

    # TODO: Once better support for multi-valued variants is added, add
    # support for auto/no/gtk2/gnome2/gtk3/motif/athena/neXtaw/photon/carbon
    variant('gui', default=False, description="build with gui (gvim)")
    variant('x', default=False, description="use the X Window System")
    depends_on('libx11', when="+x")
    depends_on('libsm', when="+x")
    depends_on('libxpm', when="+x")
    depends_on('libxt', when="+x")
    depends_on('libxtst', when="+x")

    depends_on('ncurses', when="@7.4:")

    def configure_args(self):
        spec = self.spec
        feature_set = None
        for fs in self.feature_sets:
            if "+" + fs in spec:
                if feature_set is not None:
                    raise InstallError(
                        "Only one feature set allowed, specified %s and %s"
                        % (feature_set, fs))
                feature_set = fs
        if '+gui' in spec:
            if feature_set is not None:
                if feature_set != 'huge':
                    raise InstallError(
                        "+gui variant requires 'huge' feature set, "
                        "%s was specified" % feature_set)
            feature_set = 'huge'
        if feature_set is None:
            feature_set = 'normal'

        configure_args = ["--enable-fail-if-missing"]

        configure_args.append("--with-tlib=ncursesw")

        configure_args.append("--with-features=" + feature_set)

        if '+python' in spec:
            if 'python@3:' in self.spec:
                configure_args.append("--enable-python3interp=yes")
                configure_args.append("--enable-pythoninterp=no")
            else:
                configure_args.append("--enable-python3interp=no")
                configure_args.append("--enable-pythoninterp=yes")
        else:
            configure_args.append("--enable-python3interp=no")

        if '+ruby' in spec:
            configure_args.append("--enable-rubyinterp=yes")
        else:
            configure_args.append("--enable-rubyinterp=no")

        if '+lua' in spec:
            configure_args.append("--enable-luainterp=yes")
            configure_args.append("--with-lua-prefix=%s" % spec['lua'].prefix)
        else:
            configure_args.append("--enable-luainterp=no")

        if '+perl' in spec:
            configure_args.append("--enable-perlinterp=yes")
        else:
            configure_args.append("--enable-perlinterp=no")

        if '+gui' in spec:
            configure_args.append("--enable-gui=auto")
        else:
            configure_args.append("--enable-gui=no")

        if '+x' in spec:
            configure_args.append("--with-x")
        else:
            configure_args.append("--without-x")

        if '+cscope' in spec:
            configure_args.append("--enable-cscope")

        return configure_args

    # Run the install phase with -j 1.  There seems to be a problem with
    # parallel builds that results in the creation of the links (e.g. view)
    # to the vim binary silently failing.
    def install(self, spec, prefix):
        make('install', parallel=False)
