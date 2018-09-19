##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""Test Spack's custom YAML format."""

import pytest

import spack.util.spack_yaml as syaml


@pytest.fixture()
def data():
    """Returns the data loaded from a test file"""
    test_file = """\
config_file:
  x86_64:
    foo: /path/to/foo
    bar: /path/to/bar
    baz: /path/to/baz
  some_list:
    - item 1
    - item 2
    - item 3
  another_list:
    [ 1, 2, 3 ]
  some_key: some_string
"""
    return syaml.load(test_file)


def test_parse(data):

    expected = {
        'config_file': syaml.syaml_dict([
            ('x86_64', syaml.syaml_dict([
                ('foo', '/path/to/foo'),
                ('bar', '/path/to/bar'),
                ('baz', '/path/to/baz')])),
            ('some_list', ['item 1', 'item 2', 'item 3']),
            ('another_list', [1, 2, 3]),
            ('some_key', 'some_string')
        ])}

    assert data == expected


def test_dict_order(data):

    expected_order = ['x86_64', 'some_list', 'another_list', 'some_key']
    assert list(data['config_file'].keys()) == expected_order

    expected_order = ['foo', 'bar', 'baz']
    assert list(data['config_file']['x86_64'].keys()) == expected_order


def test_line_numbers(data):
    def check(obj, start_line, end_line):
        assert obj._start_mark.line == start_line
        assert obj._end_mark.line == end_line

    check(data,                                  0, 12)
    check(data['config_file'],                   1, 12)
    check(data['config_file']['x86_64'],         2,  5)
    check(data['config_file']['x86_64']['foo'],  2,  2)
    check(data['config_file']['x86_64']['bar'],  3,  3)
    check(data['config_file']['x86_64']['baz'],  4,  4)
    check(data['config_file']['some_list'],      6,  9)
    check(data['config_file']['some_list'][0],   6,  6)
    check(data['config_file']['some_list'][1],   7,  7)
    check(data['config_file']['some_list'][2],   8,  8)
    check(data['config_file']['another_list'],  10, 10)
    check(data['config_file']['some_key'],      11, 11)


def test_yaml_aliases():
    aliased_list_1 = ['foo']
    aliased_list_2 = []
    dict_with_aliases = {
        'a': aliased_list_1,
        'b': aliased_list_1,
        'c': aliased_list_1,
        'd': aliased_list_2,
        'e': aliased_list_2,
        'f': aliased_list_2,
    }
    string = syaml.dump(dict_with_aliases)

    # ensure no YAML aliases appear in syaml dumps.
    assert '*id' not in string
