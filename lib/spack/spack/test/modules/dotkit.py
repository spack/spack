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

import functools
import pytest
import spack.modules.dotkit
import spack.modules.common


@pytest.fixture()
def patch_configuration(monkeypatch):
    def _impl(configuration):
        monkeypatch.setattr(
            spack.modules.common,
            'configuration',
            configuration
        )
        monkeypatch.setattr(
            spack.modules.dotkit,
            'configuration',
            configuration['dotkit']
        )
        monkeypatch.setattr(
            spack.modules.dotkit,
            'configuration_registry',
            {}
        )
    return _impl


@pytest.fixture()
def dotkit_modulefile(modulefile_content):
    return functools.partial(
        modulefile_content, spack.modules.dotkit.DotkitModulefileWriter
    )


@pytest.mark.usefixtures('config', 'builtin_mock')
class TestDotkit(object):
    configuration_dotkit = {
        'enable': ['dotkit'],
        'dotkit': {
            'all': {
                'autoload': 'direct'
            }
        }
    }

    def test_dotkit(self, dotkit_modulefile, patch_configuration):
        patch_configuration(self.configuration_dotkit)
        content = dotkit_modulefile('mpileaks arch=x86-linux')
        assert '#c spack' in content
        assert '#d mpileaks @2.3' in content
        assert len([x for x in content if 'dk_op' in x]) == 2
