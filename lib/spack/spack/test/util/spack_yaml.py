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
import re

import spack.config
from spack.main import SpackCommand

config_cmd = SpackCommand('config')


def get_config_line(pattern, lines):
    """Get a configuration line that matches a particular pattern."""
    line = next((l for l in lines if re.search(pattern, l)), None)
    assert line is not None, 'no such line!'
    return line


def check_blame(element, file_name, line=None):
    """Check that `config blame config` gets right file/line for an element.

    This runs `spack config blame config` and scrapes the output for a
    particular YAML key. It thne checks that the requested file/line info
    is also on that line.

    Line is optional; if it is ``None`` we just check for the
    ``file_name``, which may just be a name for a special config scope
    like ``_builtin`` or ``command_line``.
    """
    output = config_cmd('blame', 'config')

    blame_lines = output.rstrip().split('\n')
    element_line = get_config_line(element + ':', blame_lines)

    annotation = file_name
    if line is not None:
        annotation += ':%d' % line

    assert file_name in element_line


def test_config_blame(config):
    """check blame info for elements in mock configuration."""
    config_file = config.get_config_filename('site', 'config')

    check_blame('install_tree', config_file, 2)
    check_blame('source_cache', config_file, 11)
    check_blame('misc_cache', config_file, 12)
    check_blame('verify_ssl', config_file, 13)
    check_blame('checksum', config_file, 14)
    check_blame('dirty', config_file, 15)


def test_config_blame_with_override(config):
    """check blame for an element from an override scope"""
    config_file = config.get_config_filename('site', 'config')

    with spack.config.override('config:install_tree', 'foobar'):
        check_blame('install_tree', 'overrides')

        check_blame('source_cache', config_file, 11)
        check_blame('misc_cache', config_file, 12)
        check_blame('verify_ssl', config_file, 13)
        check_blame('checksum', config_file, 14)
        check_blame('dirty', config_file, 15)
