# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path
import platform
import shutil

import pytest

import llnl.util.filesystem
import spack.paths
import spack.relocate
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
