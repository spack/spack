# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import filecmp
import os
import shutil
import subprocess

import pytest

import spack.cmd
import spack.main
import spack.paths
from spack.cmd.commands import _positional_to_subroutine

commands = spack.main.SpackCommand('commands')

parser = spack.main.make_argument_parser()
spack.main.add_all_commands(parser)


def test_names():
    """Test default output of spack commands."""
    out1 = commands().strip().split('\n')
    assert out1 == spack.cmd.all_commands()
    assert 'rm' not in out1

    out2 = commands('--aliases').strip().split('\n')
    assert out1 != out2
    assert 'rm' in out2

    out3 = commands('--format=names').strip().split('\n')
    assert out1 == out3


def test_subcommands():
    """Test subcommand traversal."""
    out1 = commands('--format=subcommands')
    assert 'spack mirror create' in out1
    assert 'spack buildcache list' in out1
    assert 'spack repo add' in out1
    assert 'spack pkg diff' in out1
    assert 'spack url parse' in out1
    assert 'spack view symlink' in out1
    assert 'spack rm' not in out1
    assert 'spack compiler add' not in out1

    out2 = commands('--aliases', '--format=subcommands')
    assert 'spack mirror create' in out2
    assert 'spack buildcache list' in out2
    assert 'spack repo add' in out2
    assert 'spack pkg diff' in out2
    assert 'spack url parse' in out2
    assert 'spack view symlink' in out2
    assert 'spack rm' in out2
    assert 'spack compiler add' in out2


def test_rst():
    """Do some simple sanity checks of the rst writer."""
    out1 = commands('--format=rst')
    assert 'spack mirror create' in out1
    assert 'spack buildcache list' in out1
    assert 'spack repo add' in out1
    assert 'spack pkg diff' in out1
    assert 'spack url parse' in out1
    assert 'spack view symlink' in out1
    assert 'spack rm' not in out1
    assert 'spack compiler add' not in out1

    out2 = commands('--aliases', '--format=rst')
    assert 'spack mirror create' in out2
    assert 'spack buildcache list' in out2
    assert 'spack repo add' in out2
    assert 'spack pkg diff' in out2
    assert 'spack url parse' in out2
    assert 'spack view symlink' in out2
    assert 'spack rm' in out2
    assert 'spack compiler add' in out2


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

    commands('--update', str(update_file))
    assert update_file.exists()


def test_update_with_header(tmpdir):
    update_file = tmpdir.join('output')

    commands('--update', str(update_file))
    assert update_file.exists()
    fake_header = 'this is a header!\n\n'

    filename = tmpdir.join('header.txt')
    with filename.open('w') as f:
        f.write(fake_header)

    commands('--update', str(update_file), '--header', str(filename))


@pytest.mark.xfail
def test_no_pipe_error():
    """Make sure we don't see any pipe errors when piping output."""

    proc = subprocess.Popen(
        ['spack', 'commands', '--format=rst'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Call close() on stdout to cause a broken pipe
    proc.stdout.close()
    proc.wait()
    stderr = proc.stderr.read().decode('utf-8')

    assert 'Broken pipe' not in stderr


def test_bash_completion():
    """Test the bash completion writer."""
    out1 = commands('--format=bash')

    # Make sure header not included
    assert '_bash_completion_spack() {' not in out1
    assert '_all_packages() {' not in out1

    # Make sure subcommands appear
    assert '_spack_remove() {' in out1
    assert '_spack_compiler_find() {' in out1

    # Make sure aliases don't appear
    assert '_spack_rm() {' not in out1
    assert '_spack_compiler_add() {' not in out1

    # Make sure options appear
    assert '-h --help' in out1

    # Make sure subcommands are called
    for function in _positional_to_subroutine.values():
        assert function in out1

    out2 = commands('--aliases', '--format=bash')

    # Make sure aliases appear
    assert '_spack_rm() {' in out2
    assert '_spack_compiler_add() {' in out2


def test_update_completion_arg(tmpdir, monkeypatch):
    mock_infile = tmpdir.join("spack-completion.in")
    mock_bashfile = tmpdir.join("spack-completion.bash")

    mock_args = {
        "bash":  {
            "aliases": True,
            "format": "bash",
            "header": str(mock_infile),
            "update": str(mock_bashfile),
        },
    }

    # make a mock completion file missing the --update-completion argument
    real_args = spack.cmd.commands.update_completion_args
    shutil.copy(real_args['bash']['header'], mock_args['bash']['header'])
    with open(real_args['bash']['update']) as old:
        old_file = old.read()
        with open(mock_args['bash']['update'], 'w') as mock:
            mock.write(old_file.replace("--update-completion", ""))

    monkeypatch.setattr(
        spack.cmd.commands, 'update_completion_args', mock_args)

    # ensure things fail if --update-completion isn't specified alone
    with pytest.raises(spack.main.SpackCommandError):
        commands("--update-completion", "-a")

    # ensure arg is restored
    assert "--update-completion" not in mock_bashfile.read()
    commands("--update-completion")
    assert "--update-completion" in mock_bashfile.read()


def test_updated_completion_scripts(tmpdir):
    """Make sure our shell tab completion scripts remain up-to-date."""

    msg = ("It looks like Spack's command-line interface has been modified. "
           "Please update Spack's shell tab completion scripts by running:\n\n"
           "    spack commands --update-completion\n\n"
           "and adding the changed files to your pull request.")

    for shell in ['bash']:  # 'zsh', 'fish']:
        header = os.path.join(
            spack.paths.share_path, shell, 'spack-completion.in')
        script = 'spack-completion.{0}'.format(shell)
        old_script = os.path.join(spack.paths.share_path, script)
        new_script = str(tmpdir.join(script))

        commands('--aliases', '--format', shell,
                 '--header', header, '--update', new_script)

        assert filecmp.cmp(old_script, new_script), msg
