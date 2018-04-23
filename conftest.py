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

import pytest


# Hooks to add command line options or set other custom behaviors.
# They must be placed here to be found by pytest. See:
#
# https://docs.pytest.org/en/latest/writing_plugins.html
#
def pytest_addoption(parser):
    group = parser.getgroup("Spack specific command line options")
    group.addoption(
        '--fast', action='store_true', default=False,
        help='runs only "fast" unit tests, instead of the whole suite')


def pytest_collection_modifyitems(config, items):
    if not config.getoption('--fast'):
        # --fast not given, run all the tests
        return

    slow_tests = ['db', 'network', 'maybeslow']
    skip_as_slow = pytest.mark.skip(
        reason='skipped slow test [--fast command line option given]'
    )
    for item in items:
        if any(x in item.keywords for x in slow_tests):
            item.add_marker(skip_as_slow)
