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


class Vcsh(Package):
    """config manager based on git"""
    homepage = "https://github.com/RichiH/vcsh"
    url      = "https://github.com/RichiH/vcsh/archive/v1.20151229.tar.gz"

    version('1.20151229-1', '85c18fb15e5837d417b22980683e69ed')
    version('1.20151229', '61edf032807bba98c41c62bb2bd3d497')
    version('1.20150502', 'a6c75b5754e04bd74ae701967bb38e19')
    version('1.20141026', 'e8f42a9dbb7460f641545bea5ca1cbc4')
    version('1.20141025', '93c7fad67ab4300d76d753a32c300831')

    depends_on('git', type='run')

    # vcsh provides a makefile, if needed the install method should be adapted
    def install(self, spec, prefix):
        install('vcsh', prefix.bin)
