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

import pytest
import spack.tengine as tengine
import spack.config

from spack.util.path import canonicalize_path


class TestContext(object):

    class A(tengine.Context):
        @tengine.context_property
        def foo(self):
            return 1

    class B(tengine.Context):
        @tengine.context_property
        def bar(self):
            return 2

    class C(A, B):
        @tengine.context_property
        def foobar(self):
            return 3

        @tengine.context_property
        def foo(self):
            return 10

    def test_to_dict(self):
        """Tests that all the context properties in a hierarchy are considered
        when building the context dictionary.
        """

        # A derives directly from Context
        a = TestContext.A()
        d = a.to_dict()

        assert len(d) == 1
        assert 'foo' in d
        assert d['foo'] == 1

        # So does B
        b = TestContext.B()
        d = b.to_dict()

        assert len(d) == 1
        assert 'bar' in d
        assert d['bar'] == 2

        # C derives from both and overrides 'foo'
        c = TestContext.C()
        d = c.to_dict()

        assert len(d) == 3
        for x in ('foo', 'bar', 'foobar'):
            assert x in d

        assert d['foo'] == 10
        assert d['bar'] == 2
        assert d['foobar'] == 3


@pytest.mark.usefixtures('config')
class TestTengineEnvironment(object):

    def test_template_retrieval(self):
        """Tests the template retrieval mechanism hooked into config files"""
        # Check the directories are correct
        template_dirs = spack.config.get('config:template_dirs')
        template_dirs = [canonicalize_path(x) for x in template_dirs]
        assert len(template_dirs) == 3

        env = tengine.make_environment(template_dirs)

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
