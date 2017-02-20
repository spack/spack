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
import spack.tengine.environment as environment
import spack.config

from spack.util.path import canonicalize_path


@pytest.mark.usefixtures('config')
class TestTengineEnvironment(object):

    def test_template_retrieval(self):
        """Tests the template retrieval mechanism hooked into config files"""
        # Check the directories are correct
        template_dirs = spack.config.get_config('config')['template_dirs']
        template_dirs = [canonicalize_path(x) for x in template_dirs]
        assert len(template_dirs) == 3

        env = environment.make_environment(template_dirs)

        # Retrieve a.txt, which resides in the second
        # template directory specified in the mock configuration
        template = env.get_template('a.txt')
        text = template.render({'word': 'world'})
        assert 'Hello world!' == text

        # Retrieve b.txt, which resides in the third
        # template directory specified in the mock configuration
        template = env.get_template('b.txt')
        text = template.render({'word': 'world'})
        assert 'Howdy world!' == text
