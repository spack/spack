# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import filecmp
import os
import pathlib
import shutil
import sys
import textwrap

import pytest

import spack.cmd
import spack.cmd.commands
import spack.config
import spack.main
import spack.paths
from spack.cmd.commands import _dest_to_fish_complete, _positional_to_subroutine
from spack.util.executable import Executable


def commands(*args: str) -> str:
    """Run `spack commands args...` and return output as a string. It's a separate process so that
    we run through the main Spack command logic and avoid caching issues."""
    python = Executable(sys.executable)
    return python(spack.paths.spack_script, "commands", *args, output=str)


def test_names():
    """Test default output of spack commands."""
    out1 = commands().strip().splitlines()
    assert out1 == spack.cmd.all_commands()
    assert "rm" not in out1

    out2 = commands("--aliases").strip().splitlines()
    assert out1 != out2
    assert "rm" in out2

    out3 = commands("--format=names").strip().splitlines()
    assert out1 == out3


def test_subcommands():
    """Test subcommand traversal."""
    out1 = commands("--format=subcommands")
    assert "spack mirror create" in out1
    assert "spack buildcache list" in out1
    assert "spack repo add" in out1
    assert "spack pkg diff" in out1
    assert "spack url parse" in out1
    assert "spack view symlink" in out1
    assert "spack rm" not in out1
    assert "spack compiler add" not in out1

    out2 = commands("--aliases", "--format=subcommands")
    assert "spack mirror create" in out2
    assert "spack buildcache list" in out2
    assert "spack repo add" in out2
    assert "spack pkg diff" in out2
    assert "spack url parse" in out2
    assert "spack view symlink" in out2
    assert "spack rm" in out2
    assert "spack compiler add" in out2


def test_alias_overrides_builtin(mutable_config: spack.config.Configuration, capfd):
    """Test that spack commands cannot be overriden by aliases."""
    mutable_config.set("config:aliases", {"install": "find"})
    cmd, args = spack.main.resolve_alias("install", ["install", "-v"])
    assert cmd == "install" and args == ["install", "-v"]
    out = capfd.readouterr().err
    assert "Alias 'install' (mapping to 'find') attempts to override built-in command" in out


def test_alias_with_space(mutable_config: spack.config.Configuration, capfd):
    """Test that spack aliases with spaces are rejected."""
    mutable_config.set("config:aliases", {"foo bar": "find"})
    cmd, args = spack.main.resolve_alias("install", ["install", "-v"])
    assert cmd == "install" and args == ["install", "-v"]
    out = capfd.readouterr().err
    assert "Alias 'foo bar' (mapping to 'find') contains a space, which is not supported" in out


def test_alias_resolves_properly(mutable_config: spack.config.Configuration):
    """Test that spack aliases resolve properly."""
    mutable_config.set("config:aliases", {"my_find": "find"})
    cmd, args = spack.main.resolve_alias("my_find", ["my_find", "-v"])
    assert cmd == "find" and args == ["find", "-v"]


def test_rst():
    """Do some simple sanity checks of the rst writer."""
    out1 = commands("--format=rst")
    assert "spack mirror create" in out1
    assert "spack buildcache list" in out1
    assert "spack repo add" in out1
    assert "spack pkg diff" in out1
    assert "spack url parse" in out1
    assert "spack view symlink" in out1
    assert "spack rm" not in out1
    assert "spack compiler add" not in out1

    out2 = commands("--aliases", "--format=rst")
    assert "spack mirror create" in out2
    assert "spack buildcache list" in out2
    assert "spack repo add" in out2
    assert "spack pkg diff" in out2
    assert "spack url parse" in out2
    assert "spack view symlink" in out2
    assert "spack rm" in out2
    assert "spack compiler add" in out2


def test_rst_with_input_files(tmp_path: pathlib.Path):
    filename = tmp_path / "file.rst"
    with filename.open("w") as f:
        f.write(
            """
.. _cmd-spack-fetch:
cmd-spack-list:
.. _cmd-spack-stage:
_cmd-spack-install:
.. _cmd-spack-patch:
"""
        )

    out = commands("--format=rst", str(filename))
    for name in ["fetch", "stage", "patch"]:
        assert (":ref:`More documentation <cmd-spack-%s>`" % name) in out

    for name in ["list", "install"]:
        assert (":ref:`More documentation <cmd-spack-%s>`" % name) not in out


def test_rst_with_header(tmp_path: pathlib.Path):
    local_commands = spack.main.SpackCommand("commands")
    fake_header = "this is a header!\n\n"

    filename = tmp_path / "header.txt"
    with filename.open("w") as f:
        f.write(fake_header)

    out = local_commands("--format=rst", "--header", str(filename))
    assert out.startswith(fake_header)

    with pytest.raises(spack.main.SpackCommandError):
        local_commands("--format=rst", "--header", "asdfjhkf")


def test_rst_update(tmp_path: pathlib.Path):
    update_file = tmp_path / "output"

    commands("--update", str(update_file))
    assert update_file.exists()


def test_update_with_header(tmp_path: pathlib.Path):
    update_file = tmp_path / "output"

    commands("--update", str(update_file))
    assert update_file.exists()
    fake_header = "this is a header!\n\n"

    filename = tmp_path / "header.txt"
    with filename.open("w") as f:
        f.write(fake_header)

    commands("--update", str(update_file), "--header", str(filename))


def test_bash_completion():
    """Test the bash completion writer."""
    out1 = commands("--format=bash")

    # Make sure header not included
    assert "_bash_completion_spack() {" not in out1
    assert "_all_packages() {" not in out1

    # Make sure subcommands appear
    assert "_spack_remove() {" in out1
    assert "_spack_compiler_find() {" in out1

    # Make sure aliases don't appear
    assert "_spack_rm() {" not in out1
    assert "_spack_compiler_add() {" not in out1

    # Make sure options appear
    assert "-h --help" in out1

    # Make sure subcommands are called
    for function in _positional_to_subroutine.values():
        assert function in out1

    out2 = commands("--aliases", "--format=bash")

    # Make sure aliases appear
    assert "_spack_rm() {" in out2
    assert "_spack_compiler_add() {" in out2


def test_fish_completion():
    """Test the fish completion writer."""
    out1 = commands("--format=fish")

    # Make sure header not included
    assert "function __fish_spack_argparse" not in out1
    assert "complete -c spack --erase" not in out1

    # Make sure subcommands appear
    assert "__fish_spack_using_command remove" in out1
    assert "__fish_spack_using_command compiler find" in out1

    # Make sure aliases don't appear
    assert "__fish_spack_using_command rm" not in out1
    assert "__fish_spack_using_command compiler add" not in out1

    # Make sure options appear
    assert "-s h -l help" in out1

    # Make sure subcommands are called
    for complete_cmd in _dest_to_fish_complete.values():
        assert complete_cmd in out1

    out2 = commands("--aliases", "--format=fish")

    # Make sure aliases appear
    assert "__fish_spack_using_command rm" in out2
    assert "__fish_spack_using_command compiler add" in out2


@pytest.mark.parametrize("shell", ["bash", "fish"])
def test_update_completion_arg(shell, tmp_path: pathlib.Path, monkeypatch):
    """Test the update completion flag."""

    (tmp_path / shell).mkdir()
    mock_infile = tmp_path / shell / f"spack-completion.{shell}"
    mock_outfile = tmp_path / f"spack-completion.{shell}"

    mock_args = {
        shell: {
            "aliases": True,
            "format": shell,
            "header": str(mock_infile),
            "update": str(mock_outfile),
        }
    }

    # make a mock completion file missing the --update-completion argument
    real_args = spack.cmd.commands.update_completion_args
    shutil.copy(real_args[shell]["header"], mock_args[shell]["header"])
    with open(real_args[shell]["update"], encoding="utf-8") as old:
        old_file = old.read()
        with open(mock_args[shell]["update"], "w", encoding="utf-8") as mock:
            mock.write(old_file.replace("update-completion", ""))

    monkeypatch.setattr(spack.cmd.commands, "update_completion_args", mock_args)

    local_commands = spack.main.SpackCommand("commands")
    # ensure things fail if --update-completion isn't specified alone
    with pytest.raises(spack.main.SpackCommandError):
        local_commands("--update-completion", "-a")

    # ensure arg is restored
    assert "update-completion" not in mock_outfile.read_text()
    local_commands("--update-completion")
    assert "update-completion" in mock_outfile.read_text()


# Note: this test is never expected to be supported on Windows
@pytest.mark.not_on_windows("Shell completion script generator fails on windows")
@pytest.mark.parametrize("shell", ["bash", "fish"])
def test_updated_completion_scripts(shell, tmp_path: pathlib.Path):
    """Make sure our shell tab completion scripts remain up-to-date."""

    width = 72
    lines = textwrap.wrap(
        "It looks like Spack's command-line interface has been modified. "
        "If differences are more than your global 'include:' scopes, please "
        "update Spack's shell tab completion scripts by running:",
        width,
    )
    lines.append("\n    spack commands --update-completion\n")
    lines.extend(
        textwrap.wrap(
            "and adding the changed files (minus your global 'include:' scopes) "
            "to your pull request.",
            width,
        )
    )
    msg = "\n".join(lines)

    header = os.path.join(spack.paths.share_path, shell, f"spack-completion.{shell}")
    script = f"spack-completion.{shell}"
    old_script = os.path.join(spack.paths.share_path, script)
    new_script = str(tmp_path / script)

    commands("--aliases", "--format", shell, "--header", header, "--update", new_script)

    assert filecmp.cmp(old_script, new_script), msg
