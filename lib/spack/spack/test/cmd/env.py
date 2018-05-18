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
import unittest
import tempfile
import shutil
import pytest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import spack.cmd.env
import spack.modules
import spack.util.spack_yaml as syaml
from spack.cmd.env import (Environment, prepare_repository,
                           _environment_concretize, prepare_config_scope,
                           _environment_create)
from spack.version import Version


class TestEnvironment(unittest.TestCase):
    def setUp(self):
        self.env_dir = spack.cmd.env._db_dirname
        spack.cmd.env._db_dirname = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(spack.cmd.env._db_dirname)
        spack.cmd.env._db_dirname = self.env_dir

    def test_add(self):
        c = Environment('test')
        c.add('mpileaks')
        assert 'mpileaks' in c.user_specs

    @pytest.mark.usefixtures('config', 'mutable_mock_packages')
    def test_concretize(self):
        c = Environment('test')
        c.add('mpileaks')
        c.concretize()
        env_specs = c._get_environment_specs()
        assert any(x.name == 'mpileaks' for x in env_specs)

    @pytest.mark.usefixtures('config', 'mutable_mock_packages',
                             'install_mockery', 'mock_fetch')
    def test_env_install(self):
        c = Environment('test')
        c.add('cmake-client')
        c.concretize()
        c.install()
        env_specs = c._get_environment_specs()
        spec = next(x for x in env_specs if x.name == 'cmake-client')
        assert spec.package.installed

    @pytest.mark.usefixtures('config', 'mutable_mock_packages')
    def test_remove_after_concretize(self):
        c = Environment('test')
        c.add('mpileaks')
        c.concretize()
        c.add('python')
        c.concretize()
        c.remove('mpileaks')
        env_specs = c._get_environment_specs()
        assert not any(x.name == 'mpileaks' for x in env_specs)

    @pytest.mark.usefixtures('config', 'mutable_mock_packages')
    def test_reset_compiler(self):
        c = Environment('test')
        c.add('mpileaks')
        c.concretize()

        first_spec = c.specs_by_hash[c.concretized_order[0]]
        available = set(['gcc', 'clang'])
        available.remove(first_spec.compiler.name)
        new_compiler = next(iter(available))
        c.reset_os_and_compiler(compiler=new_compiler)

        new_spec = c.specs_by_hash[c.concretized_order[0]]
        assert new_spec.compiler != first_spec.compiler

    @pytest.mark.usefixtures('config', 'mutable_mock_packages')
    def test_environment_list(self):
        c = Environment('test')
        c.add('mpileaks')
        c.concretize()
        c.add('python')
        mock_stream = StringIO()
        c.list(mock_stream)
        list_content = mock_stream.getvalue()
        assert 'mpileaks' in list_content
        assert 'python' in list_content
        mpileaks_spec = c.specs_by_hash[c.concretized_order[0]]
        assert mpileaks_spec.format() in list_content

    @pytest.mark.usefixtures('config', 'mutable_mock_packages')
    def test_upgrade_dependency(self):
        c = Environment('test')
        c.add('mpileaks ^callpath@0.9')
        c.concretize()

        c.upgrade_dependency('callpath')
        env_specs = c._get_environment_specs()
        callpath_dependents = list(x for x in env_specs if 'callpath' in x)
        assert callpath_dependents
        for spec in callpath_dependents:
            assert spec['callpath'].version == Version('1.0')

    @pytest.mark.usefixtures('config', 'mutable_mock_packages')
    def test_init_config(self):
        test_config = """user_specs:
    - mpileaks
packages:
    mpileaks:
        version: [2.2]
"""
        spack.package_prefs.PackagePrefs._packages_config_cache = None
        spack.package_prefs.PackagePrefs._spec_cache = {}

        _environment_create('test', syaml.load(StringIO(test_config)))
        c = spack.cmd.env.read('test')
        prepare_config_scope(c)
        c.concretize()
        assert any(x.satisfies('mpileaks@2.2')
                   for x in c._get_environment_specs())

    @pytest.mark.usefixtures('config', 'mutable_mock_packages')
    def test_to_dict(self):
        c = Environment('test')
        c.add('mpileaks')
        c.concretize()
        context_dict = c.to_dict()
        c_copy = Environment.from_dict('test_copy', context_dict)
        assert c.specs_by_hash == c_copy.specs_by_hash

    @pytest.mark.usefixtures('config', 'mutable_mock_packages')
    def test_prepare_repo(self):
        c = Environment('testx')
        c.add('mpileaks')
        _environment_concretize(c)
        repo = None
        try:
            repo = prepare_repository(c)
            package = repo.get(spack.spec.Spec('mpileaks'))
            assert package.namespace.split('.')[-1] == 'testx'
        finally:
            if repo:
                shutil.rmtree(repo.root)
