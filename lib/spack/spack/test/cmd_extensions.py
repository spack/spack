# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import sys

import spack.config
import spack.extensions
import spack.main


@pytest.fixture()
def extension_root(tmpdir):
    """Create a basic extension command directory structure"""
    root = tmpdir.mkdir('spack-testcommand')
    root.ensure('testcommand', 'cmd', dir=True)
    return root


@pytest.fixture()
def single_command_extension(extension_root):
    """Simple extension command with code contained in a single file."""
    def _sce(command_name, contents):
        cmd = extension_root.ensure('testcommand', 'cmd', command_name + '.py')
        cmd.write(contents)
        return extension_root

    list_of_modules = list(sys.modules.keys())
    with spack.config.override('config:extensions', [str(extension_root)]):
        yield _sce

    to_be_deleted = [x for x in sys.modules if x not in list_of_modules]
    for module_name in to_be_deleted:
        del sys.modules[module_name]


@pytest.fixture()
def hello_world_cmd(single_command_extension):
    single_command_extension('hello-world', """
description = "hello world extension command"
section = "test command"
level = "long"

def setup_parser(subparser):
    pass


def hello_world(parser, args):
    print('Hello world!')
""")
    yield spack.main.SpackCommand('hello-world')


@pytest.fixture()
def hello_world_with_module_in_root(single_command_extension):
    """Extension command with additional code in the root folder."""
    root = single_command_extension('hello', """
# Test an absolute import
from spack.extensions.testcommand.implementation import hello_world

# Test a relative import
from ..implementation import hello_folks

description = "hello world extension command"
section = "test command"
level = "long"

# Test setting a global variable in setup_parser and retrieving
# it in the command
global_message = 'foo'

def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='subcommand')
    global global_message
    sp.add_parser('world', help='Print Hello world!')
    sp.add_parser('folks', help='Print Hello folks!')
    sp.add_parser('global', help='Print Hello folks!')
    global_message = 'bar'

def hello(parser, args):
    if args.subcommand == 'world':
        hello_world()
    elif args.subcommand == 'folks':
        hello_folks()
    elif args.subcommand == 'global':
        print(global_message)
""")
    root.ensure('testcommand', '__init__.py')
    implementation = root.ensure('testcommand', 'implementation.py')
    implementation.write("""
def hello_world():
    print('Hello world!')

def hello_folks():
    print('Hello folks!')
""")
    yield spack.main.SpackCommand('hello')


def test_simple_command_extension(hello_world_cmd):
    output = hello_world_cmd()
    assert 'Hello world!' in output


def test_command_with_import(hello_world_with_module_in_root):
    """Ensure we can write a functioning command with multiple imported
    subcommands.
    """
    output = hello_world_with_module_in_root('world')
    assert 'Hello world!' in output
    output = hello_world_with_module_in_root('folks')
    assert 'Hello folks!' in output
    output = hello_world_with_module_in_root('global')
    assert 'bar' in output


def test_missing_command():
    """Ensure that we raise the expected exception if the desired command is
    not present.
    """
    with pytest.raises(spack.extensions.CommandNotFoundError):
        spack.cmd.get_module("no-such-command")


def test_badly_named_extension():
    """Ensure that we raise the expected exception if a configured exception
    is not named according to the rules.
    """
    with pytest.raises(spack.extensions.ExtensionNamingError):
        spack.extensions.load_command_extension("oopsie", "/my/bad/extension")


@pytest.fixture()
def failing_command(single_command_extension):
    """Ensure that the configured command fails to import with the specified
    error.
    """
    def _fc(command_name, contents, exception):
        single_command_extension(command_name, contents)
        with pytest.raises(exception):
            spack.extensions.get_module(command_name)

    return _fc


# The following tests---test_failed_command_import_X)---ensure that the
# import system passes through the exception caused by attempting to
# import the failed command.
def test_failed_command_import_importerror(failing_command):
    failing_command('bad-cmd', 'from oopsie.daisy import bad\n', ImportError)


def test_failed_command_import_nameerror(failing_command):
    failing_command('bad-cmd',
                    """var = bad_function_call('blech')\n""",
                    NameError)


def test_failed_command_import_syntaxerror(failing_command):
    failing_command('bad-cmd', ')\n', SyntaxError)
