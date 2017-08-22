import unittest
import tempfile
import shutil
import pytest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import spack.cmd.context
import spack.util.spack_yaml as syaml
from spack.cmd.context import (Context, prepare_repository,
                               _context_concretize, prepare_config_scope,
                               _context_create)
from spack.version import Version

from spack.test.modules import lmod_factory  # NOQA: ignore=F401


class TestContext(unittest.TestCase):
    def setUp(self):
        self.context_dir = spack.cmd.context._db_dirname
        spack.cmd.context._db_dirname = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(spack.cmd.context._db_dirname)
        spack.cmd.context._db_dirname = self.context_dir

    def test_add(self):
        c = Context('test')
        c.add('mpileaks')
        assert 'mpileaks' in c.user_specs

    @pytest.mark.usefixtures('config', 'refresh_builtin_mock')
    def test_concretize(self):
        c = Context('test')
        c.add('mpileaks')
        c.concretize()
        env_specs = c._get_environment_specs()
        assert any(x.name == 'mpileaks' for x in env_specs)

    @pytest.mark.usefixtures('config', 'refresh_builtin_mock',
                             'install_mockery', 'mock_fetch', 'lmod_factory')
    def test_install(self):
        c = Context('test')
        c.add('cmake-client')
        c.concretize()
        c.install()
        env_specs = c._get_environment_specs()
        spec = next(x for x in env_specs if x.name == 'cmake-client')
        assert spec.package.installed
        assert c.get_modules()

    @pytest.mark.usefixtures('config', 'refresh_builtin_mock')
    def test_remove_after_concretize(self):
        c = Context('test')
        c.add('mpileaks')
        c.concretize()
        c.add('python')
        c.concretize()
        c.remove('mpileaks')
        env_specs = c._get_environment_specs()
        assert not any(x.name == 'mpileaks' for x in env_specs)

    @pytest.mark.usefixtures('config', 'refresh_builtin_mock')
    def test_reset_compiler(self):
        c = Context('test')
        c.add('mpileaks')
        c.concretize()

        first_spec = c.specs_by_hash[c.concretized_order[0]]
        available = set(['gcc', 'clang'])
        available.remove(first_spec.compiler.name)
        new_compiler = next(iter(available))
        c.reset_os_and_compiler(compiler=new_compiler)

        new_spec = c.specs_by_hash[c.concretized_order[0]]
        assert new_spec.compiler != first_spec.compiler

    @pytest.mark.usefixtures('config', 'refresh_builtin_mock')
    def test_context_list(self):
        c = Context('test')
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

    @pytest.mark.usefixtures('config', 'refresh_builtin_mock')
    def test_upgrade_dependency(self):
        c = Context('test')
        c.add('mpileaks ^callpath@0.9')
        c.concretize()

        c.upgrade_dependency('callpath')
        env_specs = c._get_environment_specs()
        callpath_dependents = list(x for x in env_specs if 'callpath' in x)
        assert callpath_dependents
        for spec in callpath_dependents:
            assert spec['callpath'].version == Version('1.0')

    @pytest.mark.usefixtures('config', 'refresh_builtin_mock')
    def test_init_config(self):
        test_config = """user_specs:
    - mpileaks
packages:
    mpileaks:
        version: [2.2]
"""
        spack.package_prefs.PackagePrefs._packages_config_cache = None
        spack.package_prefs.PackagePrefs._spec_cache = {}

        _context_create('test', syaml.load(StringIO(test_config)))
        c = spack.cmd.context.read('test')
        prepare_config_scope(c)
        c.concretize()
        assert any(x.satisfies('mpileaks@2.2')
                   for x in c._get_environment_specs())

    @pytest.mark.usefixtures('config', 'refresh_builtin_mock')
    def test_to_dict(self):
        c = Context('test')
        c.add('mpileaks')
        c.concretize()
        context_dict = c.to_dict()
        c_copy = Context.from_dict('test_copy', context_dict)
        assert c.specs_by_hash == c_copy.specs_by_hash

    @pytest.mark.usefixtures('config', 'refresh_builtin_mock')
    def test_prepare_repo(self):
        c = Context('testx')
        c.add('mpileaks')
        _context_concretize(c)
        repo = None
        try:
            repo = prepare_repository(c)
            package = repo.get(spack.spec.Spec('mpileaks'))
            assert package.namespace.split('.')[-1] == 'testx'
        finally:
            if repo:
                shutil.rmtree(repo.root)
