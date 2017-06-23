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
import os


class NinjaFortran(Package):
    """ A Fortran capable fork of ninja """
    homepage = "https://github.com/Kitware/ninja"
    url      = "https://github.com/Kitware/ninja/archive/v1.7.2.gcc0ea.kitware.dyndep-1.tar.gz"

    version('1.7.2', '3982f508c415c0abaca34cb5e92e711a')

    extends('python')

    def url_for_version(self, version):
        url = 'https://github.com/Kitware/ninja/archive/v{0}.gcc0ea.kitware.dyndep-1.tar.gz'
        return url.format(version)

    def install(self, spec, prefix):
        python('configure.py', '--bootstrap')

        mkdir(prefix.bin)
        install('ninja', prefix.bin)
        install_tree('misc', join_path(prefix, 'misc'))
        with working_dir(prefix.bin):
            os.symlink('ninja', 'ninja-build')
