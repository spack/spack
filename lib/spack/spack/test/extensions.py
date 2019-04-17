# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    with spack.config.override('config:extensions', [str(extension_root)]):
        yield spack.main.SpackCommand('hello')

    del sys.modules['spack.extensions.testcommand']
    del sys.modules['spack.extensions.testcommand.cmd']


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

def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='subcommand')
    world = sp.add_parser('world', help='Print Hello world!')
    folks = sp.add_parser('folks', help='Print Hello folks!')


def hello(parser, args):
    if args.subcommand == 'world':
        hello_world()
    elif args.subcommand == 'folks':
        hello_folks()
""")
    implementation = extension_root.ensure('testcommand', 'implementation.py')
    implementation.write("""
def hello_world():
    print('Hello world!')

def hello_folks():
    print('Hello folks!')
""")
    with spack.config.override('config:extensions', [str(extension_root)]):
        yield spack.main.SpackCommand('hello')

    del sys.modules['spack.extensions.testcommand']
    del sys.modules['spack.extensions.testcommand.implementation']
    del sys.modules['spack.extensions.testcommand.cmd']


def test_simple_command_extension(hello_world_cmd):
    output = hello_world_cmd()
    assert 'Hello world!' in output


def test_subcommand_in_nested_directory(hello_world_with_module_in_root):
    output = hello_world_with_module_in_root('world')
    assert 'Hello world!' in output
    output = hello_world_with_module_in_root('folks')
    assert 'Hello folks!' in output
