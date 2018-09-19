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
import os


class Global(Package):
    """ The Gnu Global tagging system """

    homepage = "http://www.gnu.org/software/global"
    url = "http://tamacom.com/global/global-6.5.tar.gz"

    version('6.5', 'dfec818b4f53d91721e247cf7b218078')

    depends_on('exuberant-ctags', type=('build', 'run'))
    depends_on('ncurses')

    def install(self, spec, prefix):
        config_args = ['--prefix={0}'.format(prefix)]

        config_args.append('--with-exuberant-ctags={0}'.format(
            os.path.join(spec['exuberant-ctags'].prefix.bin, 'ctags')))

        configure(*config_args)

        make()
        make("install")
