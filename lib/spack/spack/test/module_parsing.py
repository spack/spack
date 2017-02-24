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
import pytest
from spack.util.module_cmd import get_argument_from_module_line


def test_get_argument_from_module_line():
    lines = ['prepend-path LD_LIBRARY_PATH /lib/path',
             'prepend-path  LD_LIBRARY_PATH  /lib/path',
             "prepend_path('PATH' , '/lib/path')",
             'prepend_path( "PATH" , "/lib/path" )',
             'prepend_path("PATH",' + "'/lib/path')"]

    bad_lines = ['prepend_path(PATH,/lib/path)',
                 'prepend-path (LD_LIBRARY_PATH) /lib/path']

    assert all(get_argument_from_module_line(l) == '/lib/path' for l in lines)
    for bl in bad_lines:
        with pytest.raises(ValueError):
            get_argument_from_module_line(bl)
