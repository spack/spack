# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from spack.main import SpackCommand


@pytest.mark.xfail
def test_reuse_after_help():
    """Test `spack help` can be called twice with the same SpackCommand."""
    help_cmd = SpackCommand('help')
    help_cmd()

    # This second invocation will somehow fail because the parser no
    # longer works after add_all_commands() is called in
    # SpackArgumentParser.format_help_sections().
    #
    # TODO: figure out why this doesn't work properly and change this
    # test to use a single SpackCommand.
    #
    # It seems that parse_known_args() finds "too few arguments" the
    # second time through b/c add_all_commands() ends up leaving extra
    # positionals in the parser. But this used to work before we loaded
    # commands lazily.
    help_cmd()


def test_help():
    """Sanity check the help command to make sure it works."""
    help_cmd = SpackCommand('help')
    out = help_cmd()
    assert 'These are common spack commands:' in out


def test_help_all():
    """Test the spack help --all flag"""
    help_cmd = SpackCommand('help')
    out = help_cmd('--all')
    assert 'Complete list of spack commands:' in out


def test_help_spec():
    """Test the spack help --spec flag"""
    help_cmd = SpackCommand('help')
    out = help_cmd('--spec')
    assert 'spec expression syntax:' in out


def test_help_subcommand():
    """Test the spack help subcommand argument"""
    help_cmd = SpackCommand('help')
    out = help_cmd('help')
    assert 'get help on spack and its commands' in out
