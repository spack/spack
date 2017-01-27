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
# import pytest
from spack.cmd.url import *


# @pytest.fixture(scope='url')
# def parser():
#     """Returns the parser for the ``url`` command"""
#     parser = argparse.ArgumentParser()
#     setup_parser(parser)
#     return parser


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
    assert not name_parsed_correctly(MyPackage('imagemagick', []), 'ImageMagick')  # noqa
    assert not name_parsed_correctly(MyPackage('yaml-cpp',    []), 'yamlcpp')
    assert not name_parsed_correctly(MyPackage('yamlcpp',     []), 'yaml-cpp')
    assert not name_parsed_correctly(MyPackage('r-py-parser', []), 'parser')
    assert not name_parsed_correctly(MyPackage('oce',         []), 'oce-0.18.0')   # noqa


def test_version_parsed_correctly():
    # Expected True
    assert version_parsed_correctly(Package('', ['1.2.3']),        '1.2.3')
    assert version_parsed_correctly(Package('', ['5.4a', '5.4b']), '5.4a')

    # Expected False
    assert not version_parsed_correctly(Package('', ['0.18.0']), 'oce-0.18.0')


# def test_url_parse(parser):
#     args = parser.parse_args(['parse', 'http://zlib.net/fossils/zlib-1.2.10.tar.gz'])
#     spack.cmd.url.url(parser, args)
