##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class HasPathAttr(Package):
    homepage = "http://www.example.com"
    url      = "http://www.example.com/has-path-attr-0.8.13.tar.gz"

    version('1.3.0', '4136d7b4c04df68b686570afa26988ac')
    version('1.2.0', 'e21f8273d9f5f6d43a59878dc274fec7')
    version('1.1.0', '9db4d36c283d9790d8fa7df1f4d7b4d9')

    simple_path_list = 'include'
    short_version_path_list = "example/pkg-{version.up_to(2)}"
    long_version_path_list = "example/pkg-{version.up_to(3)}"
    subdir_list_path_list = ['lib64', 'lib/hasattr-{version.up_to(3)}']
    plain_list_path_list = ['lib64', 'lib']

    def install(self, spec, prefix):
        pass
