# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections
import os.path
import platform
import shutil

import llnl.util.filesystem
import pytest
import spack.architecture
import spack.concretize
import spack.paths
import spack.relocate
import spack.spec
import spack.store
import spack.tengine
import spack.util.executable


@pytest.fixture(params=[True, False])
def is_relocatable(request):
    return request.param


@pytest.fixture()
def source_file(tmpdir, is_relocatable):
    """Returns the path to a source file of a relocatable executable."""
    if is_relocatable:
        template_src = os.path.join(
            spack.paths.test_path, 'data', 'templates', 'relocatable.c'
        )
        src = tmpdir.join('relocatable.c')
        shutil.copy(template_src, str(src))
    else:
        template_dirs = [
            os.path.join(spack.paths.test_path, 'data', 'templates')
        ]
        env = spack.tengine.make_environment(template_dirs)
        template = env.get_template('non_relocatable.c')
        text = template.render({'prefix': spack.store.layout.root})

        src = tmpdir.join('non_relocatable.c')
        src.write(text)

    return src


@pytest.fixture(params=['which_found', 'installed', 'to_be_installed'])
def expected_patchelf_path(request, mutable_database, monkeypatch):
    """Prepare the stage to tests different cases that can occur
    when searching for patchelf.
    """
    case = request.param

    # Mock the which function
    which_fn = {
        'which_found': lambda x: collections.namedtuple(
            '_', ['path']
        )('/usr/bin/patchelf')
    }
    monkeypatch.setattr(
        spack.util.executable, 'which',
        which_fn.setdefault(case, lambda x: None)
    )
    if case == 'which_found':
        return '/usr/bin/patchelf'

    # TODO: Mock a case for Darwin architecture

    spec = spack.spec.Spec('patchelf')
    spec.concretize()

    patchelf_cls = type(spec.package)
    do_install = patchelf_cls.do_install
    expected_path = os.path.join(spec.prefix.bin, 'patchelf')

    def do_install_mock(self, **kwargs):
        do_install(self, fake=True)
        with open(expected_path):
            pass

    monkeypatch.setattr(patchelf_cls, 'do_install', do_install_mock)
    if case == 'installed':
        spec.package.do_install()

    return expected_path


@pytest.fixture()
def mock_patchelf(tmpdir):
    import jinja2

    def _factory(output):
        f = tmpdir.mkdir('bin').join('patchelf')
        t = jinja2.Template('#!/bin/bash\n{{ output }}\n')
        f.write(t.render(output=output))
        f.chmod(0o755)
        return str(f)

    return _factory


@pytest.mark.requires_executables(
    '/usr/bin/gcc', 'patchelf', 'strings', 'file'
)
def test_file_is_relocatable(source_file, is_relocatable):
    compiler = spack.util.executable.Executable('/usr/bin/gcc')
    executable = str(source_file).replace('.c', '.x')
    compiler_env = {
        'PATH': '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
    }
    compiler(str(source_file), '-o', executable, env=compiler_env)

    assert spack.relocate.is_binary(executable)
    assert spack.relocate.file_is_relocatable(executable) is is_relocatable


@pytest.mark.requires_executables(
    'patchelf', 'strings', 'file'
)
def test_patchelf_is_relocatable():
    patchelf = spack.relocate._patchelf()
    assert llnl.util.filesystem.is_exe(patchelf)
    assert spack.relocate.file_is_relocatable(patchelf)


@pytest.mark.skipif(
    platform.system().lower() != 'linux',
    reason='implementation for MacOS still missing'
)
def test_file_is_relocatable_errors(tmpdir):
    # The file passed in as argument must exist...
    with pytest.raises(ValueError) as exc_info:
        spack.relocate.file_is_relocatable('/usr/bin/does_not_exist')
    assert 'does not exist' in str(exc_info.value)

    # ...and the argument must be an absolute path to it
    file = tmpdir.join('delete.me')
    file.write('foo')

    with llnl.util.filesystem.working_dir(str(tmpdir)):
        with pytest.raises(ValueError) as exc_info:
            spack.relocate.file_is_relocatable('delete.me')
        assert 'is not an absolute path' in str(exc_info.value)


@pytest.mark.skipif(
    platform.system().lower() != 'linux',
    reason='implementation for MacOS still missing'
)
def test_search_patchelf(expected_patchelf_path):
    current = spack.relocate._patchelf()
    assert current == expected_patchelf_path


@pytest.mark.parametrize('patchelf_behavior,expected', [
    ('echo ', []),
    ('echo /opt/foo/lib:/opt/foo/lib64', ['/opt/foo/lib', '/opt/foo/lib64']),
    ('exit 1', [])
])
def test_existing_rpaths(patchelf_behavior, expected, mock_patchelf):
    # Here we are mocking an executable that is always called "patchelf"
    # because that will skip the part where we try to build patchelf
    # by ourselves. The executable will output some rpaths like
    # `patchelf --print-rpath` would.
    path = mock_patchelf(patchelf_behavior)
    rpaths = spack.relocate._elf_rpaths_for(path)
    assert rpaths == expected


@pytest.mark.parametrize('start_path,path_root,paths,expected', [
    ('/usr/bin/test', '/usr', ['/usr/lib', '/usr/lib64', '/opt/local/lib'],
     ['$ORIGIN/../lib', '$ORIGIN/../lib64', '/opt/local/lib'])
])
def test_make_relative_paths(start_path, path_root, paths, expected):
    relatives = spack.relocate._make_relative(start_path, path_root, paths)
    assert relatives == expected


@pytest.mark.parametrize('start_path,relative_paths,expected', [
    # $ORIGIN will be replaced with os.path.dirname('usr/bin/test')
    # and then normalized
    ('/usr/bin/test',
     ['$ORIGIN/../lib', '$ORIGIN/../lib64', '/opt/local/lib'],
     ['/usr/lib', '/usr/lib64', '/opt/local/lib']),
    # Relative path without $ORIGIN
    ('/usr/bin/test', ['../local/lib'], ['../local/lib']),
])
def test_normalize_relative_paths(start_path, relative_paths, expected):
    normalized = spack.relocate._normalize_relative_paths(
        start_path, relative_paths
    )
    assert normalized == expected
