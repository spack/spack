# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import sys

import spack.cmd
import spack.config
import spack.extensions
import spack.main


class Extension:
    def __init__(self, name, root):
        self.name = name
        self.pname = spack.cmd.python_name(name)
        self.root = root
        self.main = self.root.ensure(self.pname, dir=True)
        self.cmd = self.main.ensure('cmd', dir=True)

    def add_command(self, command_name, contents):
        spack.cmd.require_cmd_name(command_name)
        python_name = spack.cmd.python_name(command_name)
        cmd = self.cmd.ensure(python_name + '.py')
        cmd.write(contents)


@pytest.fixture(params=['testcommand'])
def extension(request, tmpdir):
    """Create a basic extension command directory structure"""
    extension_name = request.param
    root = tmpdir.mkdir('spack-' + extension_name)
    extension = Extension(extension_name, root)

    list_of_modules = list(sys.modules.keys())
    with spack.config.override('config:extensions', [str(extension.root)]):
        yield extension

    to_be_deleted = [x for x in sys.modules if x not in list_of_modules]
    for module_name in to_be_deleted:
        del sys.modules[module_name]


@pytest.fixture()
def hello_world_extension(extension):
    """Create an extension with a hello-world command."""
    extension.add_command('hello-world', """
description = "hello world extension command"
section = "test command"
level = "long"

def setup_parser(subparser):
    pass


def hello_world(parser, args):
    print('Hello world!')
""")
    yield extension


@pytest.fixture()
def hello_world_cmd(hello_world_extension):
    """Create and return an invokable "hello-world" extension command."""
    yield spack.main.SpackCommand('hello-world')


@pytest.fixture()
def hello_world_with_module_in_root(extension):
    """Create a "hello-world" extension command with additional code in the
    root folder.
    """

    # Note that the namespace of the extension is derived from the
    # fixture.
    extension.add_command('hello', """
# Test an absolute import
from spack.extensions.{ext_pname}.implementation import hello_world

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
""".format(ext_pname=extension.pname))

    extension.main.ensure('__init__.py')
    implementation \
        = extension.main.ensure('implementation.py')
    implementation.write("""
def hello_world():
    print('Hello world!')

def hello_folks():
    print('Hello folks!')
""")
    yield spack.main.SpackCommand('hello')


def test_simple_command_extension(hello_world_cmd):
    """Basic test of a functioning command."""
    output = hello_world_cmd()
    assert 'Hello world!' in output


def test_multi_extension_search(hello_world_extension, tmpdir):
    """Ensure we can find an extension command even if it's not in the first
    place we look.
    """

    extra_ext_name = 'testcommand2'
    extra_ext = Extension(extra_ext_name,
                          tmpdir.mkdir('spack-' + extra_ext_name))
    with spack.config.override('config:extensions',
                               [str(extra_ext.root),
                                str(hello_world_extension.root)]):
        assert ('Hello world') in spack.main.SpackCommand('hello-world')()


def test_duplicate_module_load(hello_world_cmd):
    """Ensure duplicate module load attempts are successful.

    The command module will already have been loaded once by the
    hello_world_cmd fixture.
    """
    assert ('Hello world') in spack.main.SpackCommand('hello-world')()


@pytest.mark.parametrize('extension',
                         ['testcommand', 'hyphenated-extension'],
                         ids=['simple', 'hyphenated_extension_name'],
                         indirect=True)
def test_command_with_import(hello_world_with_module_in_root):
    """Ensure we can write a functioning command with multiple imported
    subcommands, including where the extension name contains a hyphen.
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


@pytest.mark.parametrize('extension_data',
                         [('/my/bad/extension', False),
                          ('', False),
                          ('/my/bad/spack--extra-hyphen', False),
                          ('/my/good/spack-extension', True),
                          ('/my/still/good/spack-extension/', True),
                          ('/my/spack-hyphenated-extension', True)],
                         ids=['no_stem', 'vacuous', 'leading_hyphen',
                              'basic_good', 'trailing_slash', 'hyphenated'])
def test_extension_naming(extension_data):
    """Ensure that we are correctly validating configured extension paths
    for conformity with the rules: basename match ``spack-<name>''; name may
    have embedded extensions but not begin with one.
    """
    ext_path = extension_data[0]
    expected_exception\
        = spack.extensions.CommandNotFoundError if \
        extension_data[1] else \
        spack.extensions.ExtensionNamingError
    with spack.config.override('config:extensions',
                               [ext_path]), pytest.raises(expected_exception):
        spack.cmd.get_module("no-such-command")


def test_missing_command_function(extension):
    """Ensure we die as expected if a command module does not have the
    expected command function defined.
    """
    extension.add_command('bad-cmd', """
description = "Empty command implementation"\n""")
    with pytest.raises(SystemExit, matches="must define function 'bad-cmd'."):
        spack.cmd.get_module('bad-cmd')


@pytest.fixture()
def failing_command(extension):
    """Ensure that the configured command fails to import with the specified
    error.
    """
    def _fc(command_name, contents, exception):
        extension.add_command(command_name, contents)
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
