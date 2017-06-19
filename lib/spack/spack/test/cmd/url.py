##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import argparse
import pytest

from spack.cmd.url import *


@pytest.fixture(scope='module')
def parser():
    """Returns the parser for the ``url`` command"""
    parser = argparse.ArgumentParser()
    setup_parser(parser)
    return parser


class MyPackage:
    def __init__(self, name, versions):
        self.name = name
        self.versions = versions


def test_name_parsed_correctly():
    # Expected True
    assert name_parsed_correctly(MyPackage('netcdf',         []), 'netcdf')
    assert name_parsed_correctly(MyPackage('r-devtools',     []), 'devtools')
    assert name_parsed_correctly(MyPackage('py-numpy',       []), 'numpy')
    assert name_parsed_correctly(MyPackage('octave-splines', []), 'splines')

    # Expected False
    assert not name_parsed_correctly(MyPackage('',            []), 'hdf5')
    assert not name_parsed_correctly(MyPackage('hdf5',        []), '')
    assert not name_parsed_correctly(MyPackage('imagemagick', []), 'ImageMagick')  # noqa
    assert not name_parsed_correctly(MyPackage('yaml-cpp',    []), 'yamlcpp')
    assert not name_parsed_correctly(MyPackage('yamlcpp',     []), 'yaml-cpp')
    assert not name_parsed_correctly(MyPackage('r-py-parser', []), 'parser')
    assert not name_parsed_correctly(MyPackage('oce',         []), 'oce-0.18.0')   # noqa


def test_version_parsed_correctly():
    # Expected True
    assert version_parsed_correctly(MyPackage('', ['1.2.3']),        '1.2.3')
    assert version_parsed_correctly(MyPackage('', ['5.4a', '5.4b']), '5.4a')
    assert version_parsed_correctly(MyPackage('', ['5.4a', '5.4b']), '5.4b')

    # Expected False
    assert not version_parsed_correctly(MyPackage('', []),         '1.2.3')
    assert not version_parsed_correctly(MyPackage('', ['1.2.3']),  '')
    assert not version_parsed_correctly(MyPackage('', ['1.2.3']),  '1.2.4')
    assert not version_parsed_correctly(MyPackage('', ['3.4a']),   '3.4')
    assert not version_parsed_correctly(MyPackage('', ['3.4']),    '3.4b')
    assert not version_parsed_correctly(MyPackage('', ['0.18.0']), 'oce-0.18.0')   # noqa


def test_url_parse(parser):
    args = parser.parse_args(['parse', 'http://zlib.net/fossils/zlib-1.2.10.tar.gz'])
    url(parser, args)


@pytest.mark.xfail
def test_url_parse_xfail(parser):
    # No version in URL
    args = parser.parse_args(['parse', 'http://www.netlib.org/voronoi/triangle.zip'])
    url(parser, args)


def test_url_list(parser):
    args = parser.parse_args(['list'])
    total_urls = url_list(args)

    # The following two options should not change the number of URLs printed.
    args = parser.parse_args(['list', '--color', '--extrapolation'])
    colored_urls = url_list(args)
    assert colored_urls == total_urls

    # The following two options should print fewer URLs than the default.
    # If they print the same number of URLs, something is horribly broken.
    # If they say we missed 0 URLs, something is probably broken too.
    args = parser.parse_args(['list', '--incorrect-name'])
    incorrect_name_urls = url_list(args)
    assert 0 < incorrect_name_urls < total_urls

    args = parser.parse_args(['list', '--incorrect-version'])
    incorrect_version_urls = url_list(args)
    assert 0 < incorrect_version_urls < total_urls


def test_url_test(parser):
    args = parser.parse_args(['test'])
    (total_urls, correct_names, correct_versions,
     name_count_dict, version_count_dict) = url_test(args)

    assert 0 < correct_names    <= sum(name_count_dict.values())    <= total_urls  # noqa
    assert 0 < correct_versions <= sum(version_count_dict.values()) <= total_urls  # noqa
