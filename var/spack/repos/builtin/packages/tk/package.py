##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Tk(AutotoolsPackage):
    """Tk is a graphical user interface toolkit that takes developing
       desktop applications to a higher level than conventional
       approaches. Tk is the standard GUI not only for Tcl, but for
       many other dynamic languages, and can produce rich, native
       applications that run unchanged across Windows, Mac OS X, Linux
       and more."""
    homepage = "http://www.tcl.tk"

    version('8.6.6', 'dd7dbb3a6523c42d05f6ab6e86096e99')
    version('8.6.5', '11dbbd425c3e0201f20d6a51482ce6c4')
    version('8.6.3', '85ca4dbf4dcc19777fd456f6ee5d0221')

    variant('X', default=False, description='Enable X11 support')

    depends_on("tcl")
    depends_on("libx11", when='+X')

    configure_directory = 'unix'

    def url_for_version(self, version):
        base_url = "http://prdownloads.sourceforge.net/tcl"
        return "{0}/tk{1}-src.tar.gz".format(base_url, version)

    def setup_environment(self, spack_env, run_env):
        # When using Tkinter from within spack provided python+tk, python
        # will not be able to find Tcl/Tk unless TK_LIBRARY is set.
        run_env.set('TK_LIBRARY', join_path(self.prefix.lib, 'tk{0}'.format(
            self.spec.version.up_to(2))))

    def configure_args(self):
        spec = self.spec
        return ['--with-tcl={0}'.format(spec['tcl'].prefix.lib)]
