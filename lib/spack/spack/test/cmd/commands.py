# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import pytest

from llnl.util.argparsewriter import ArgparseWriter

from spack.command_loading import all_commands
import spack.main

commands = spack.main.SpackCommand('commands')

parser = spack.main.make_argument_parser()
spack.main.add_all_commands(parser)


def test_commands_by_name():
    """Test default output of spack commands."""
    out = commands()
    assert out.strip().split('\n') == sorted(all_commands())


def test_subcommands():
    """Test subcommand traversal."""
    out = commands('--format=subcommands')
    assert 'spack mirror create' in out
    assert 'spack buildcache list' in out
    assert 'spack repo add' in out
    assert 'spack pkg diff' in out
    assert 'spack url parse' in out
    assert 'spack view symlink' in out

    class Subcommands(ArgparseWriter):
        def begin_command(self, prog):
            assert prog in out

    Subcommands().write(parser)


def test_rst():
    """Do some simple sanity checks of the rst writer."""
    out = commands('--format=rst')

    class Subcommands(ArgparseWriter):
        def begin_command(self, prog):
            assert prog in out
            assert re.sub(r' ', '-', prog) in out
    Subcommands().write(parser)


def test_rst_with_input_files(tmpdir):
    filename = tmpdir.join('file.rst')
    with filename.open('w') as f:
        f.write('''
.. _cmd-spack-fetch:
cmd-spack-list:
.. _cmd-spack-stage:
_cmd-spack-install:
.. _cmd-spack-patch:
''')

    out = commands('--format=rst', str(filename))
    for name in ['fetch', 'stage', 'patch']:
        assert (':ref:`More documentation <cmd-spack-%s>`' % name) in out

    for name in ['list', 'install']:
        assert (':ref:`More documentation <cmd-spack-%s>`' % name) not in out


def test_rst_with_header(tmpdir):
    fake_header = 'this is a header!\n\n'

    filename = tmpdir.join('header.txt')
    with filename.open('w') as f:
        f.write(fake_header)

    out = commands('--format=rst', '--header', str(filename))
    assert out.startswith(fake_header)

    with pytest.raises(spack.main.SpackCommandError):
        commands('--format=rst', '--header', 'asdfjhkf')


def test_rst_update(tmpdir):
    update_file = tmpdir.join('output')

    # not yet created when commands is run
    commands('--update', str(update_file))
    assert update_file.exists()
    with update_file.open() as f:
        assert f.read()

    # created but older than commands
    with update_file.open('w') as f:
        f.write('empty\n')
    update_file.setmtime(0)
    commands('--update', str(update_file))
    assert update_file.exists()
    with update_file.open() as f:
        assert f.read() != 'empty\n'

    # newer than commands
    with update_file.open('w') as f:
        f.write('empty\n')
    commands('--update', str(update_file))
    assert update_file.exists()
    with update_file.open() as f:
        assert f.read() == 'empty\n'
