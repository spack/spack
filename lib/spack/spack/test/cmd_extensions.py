# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import sys

import spack.config
import spack.main


@pytest.fixture()
def extension_root(tmpdir):
    root = tmpdir.mkdir('spack-testcommand')
    root.ensure('testcommand', 'cmd', dir=True)
    return root


@pytest.fixture()
def hello_world_cmd(extension_root):
    """Simple extension command with code contained in a single file."""
    hello = extension_root.ensure('testcommand', 'cmd', 'hello.py')
    hello.write("""
description = "hello world extension command"
section = "test command"
level = "long"

def setup_parser(subparser):
    pass


def hello(parser, args):
    print('Hello world!')
""")
    list_of_modules = list(sys.modules.keys())
    with spack.config.override('config:extensions', [str(extension_root)]):
        yield spack.main.SpackCommand('hello')

    to_be_deleted = [x for x in sys.modules if x not in list_of_modules]
    for module_name in to_be_deleted:
        del sys.modules[module_name]


@pytest.fixture()
def hello_world_with_module_in_root(extension_root):
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
