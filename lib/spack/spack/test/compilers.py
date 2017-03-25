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

import spack.spec
import spack.compilers as compilers


@pytest.mark.usefixtures('config')
class TestCompilers(object):
    
    def test_get_compiler_duplicates(self):
        # In this case there is only one instance of the specified compiler in
        # the test configuration (so it is not actually a duplicate), but the
        # method behaves the same.
        cfg_file_to_duplicates = compilers.get_compiler_duplicates(
            'gcc@4.5.0', spack.spec.ArchSpec('cray-CNL-xeon'))
        assert len(cfg_file_to_duplicates) == 1
        cfg_file, duplicates = cfg_file_to_duplicates.iteritems().next()
        assert len(duplicates) == 1

    def test_all_compilers(self):
        all_compilers = compilers.all_compilers()
        filtered = list(x for x in all_compilers if str(x.spec) == 'clang@3.3')
        filtered = list(x for x in filtered if x.operating_system == 'SuSE11')
        assert len(filtered) == 1
