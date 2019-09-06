# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import sys

from spack.command_loading import get_command_module_from
import spack.config
import spack.main
import spack.extensions


@pytest.fixture()
def extension_root(tmpdir):
    root = tmpdir.mkdir('spack-testcommand')
    root.ensure('testcommand', 'cmd', dir=True)
    return root


_hello_world_cmd_text = """
description = "hello world extension command"
section = "test command"
level = "long"

def setup_parser(subparser):
    pass


def hello(parser, args):
    print('Hello world!')
"""


@pytest.fixture()
def clean_extension_command_map(monkeypatch):
    monkeypatch.setattr(spack.extensions, '_extension_command_map', None)
    yield


@pytest.fixture()
def hello_world_cmd(extension_root, clean_extension_command_map):
    """Simple extension command with code contained in a single file."""
    hello = extension_root.ensure('testcommand', 'cmd', 'hello.py')
    hello.write(_hello_world_cmd_text)
    list_of_modules = list(sys.modules.keys())
    with spack.config.override('config:extensions', [str(extension_root)]):
        yield spack.main.SpackCommand('hello')

    to_be_deleted = [x for x in sys.modules if x not in list_of_modules]
    for module_name in to_be_deleted:
        del sys.modules[module_name]


@pytest.fixture()
def hello_world_with_module_in_root(extension_root,
                                    clean_extension_command_map):
    """Extension command with additional code in the root folder."""
    extension_root.ensure('testcommand', '__init__.py')
    command_root = extension_root.join('testcommand', 'cmd')
    hello = command_root.ensure('hello.py')
    hello.write("""
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
    implementation = extension_root.ensure('testcommand', 'implementation.py')
    implementation.write("""
def hello_world():
    print('Hello world!')

def hello_folks():
    print('Hello folks!')
""")
    list_of_modules = list(sys.modules.keys())
    with spack.config.override('config:extensions', [str(extension_root)]):
        yield spack.main.SpackCommand('hello')

    to_be_deleted = [x for x in sys.modules if x not in list_of_modules]
    for module_name in to_be_deleted:
        del sys.modules[module_name]


@pytest.fixture()
def subcommand_root(tmpdir):
    root = tmpdir.mkdir('subcommand_root')
    return root


def _ensure_package(base, *parts):
    """Ensure that all the components of a module directory path exist, and
    contain a file __init__.py."""
    bits = []
    for bit in parts[:-1]:
        bits.append(bit)
        base.ensure(*(bits + ['__init__.py']))
    return base.ensure(*parts)


@pytest.fixture()
def hello_world_sub_no_cmd(subcommand_root):
    """Failed attempt at a subcommand (bad location)."""
    hello = _ensure_package(subcommand_root, 'bad', 'hello.py')
    hello.write(_hello_world_cmd_text)
    sys.path.insert(0, str(subcommand_root))
    yield
    sys.path.remove(str(subcommand_root))


@pytest.fixture()
def hello_world_sub_cmd(subcommand_root):
    """Simulated subcommand."""
    hello = _ensure_package(subcommand_root, 'good', 'cmd', 'hello.py')
    hello.write(_hello_world_cmd_text)
    sys.path.insert(0, str(subcommand_root))
    yield
    sys.path.remove(str(subcommand_root))


def test_simple_command_extension(hello_world_cmd):
    output = hello_world_cmd()
    assert 'Hello world!' in output


def test_command_with_import(hello_world_with_module_in_root):
    output = hello_world_with_module_in_root('world')
    assert 'Hello world!' in output
    output = hello_world_with_module_in_root('folks')
    assert 'Hello folks!' in output
    output = hello_world_with_module_in_root('global')
    assert 'bar' in output


def test_cmd_module(hello_world_sub_cmd):
    get_command_module_from('hello', 'good')


def test_missing_cmd_module(hello_world_sub_no_cmd):
    """Ensure that we raise an exception in get_command_module_from() if we
    cannot load the specified module."""
    expected_message\
        = 'No module named {0}'.\
        format('cmd.hello' if sys.version_info[0] < 3 else "'bad.cmd'")
    with pytest.raises(ImportError) as e:
        get_command_module_from('hello', 'bad')
    assert str(e.value) == expected_message
