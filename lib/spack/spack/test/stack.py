##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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

import collections as c
import spack.cmd.stack
import spack.store
import spack.test.conftest


def test_stack(database, refresh_db_on_exit, install_mockery):
    """Ensure that stacked packages appear in second database.
    """
    remote = str(database.mock.path)

    arg_t = c.namedtuple(
        "Arguments",
        ["remotes", "exclude", "nostack", "hardlinks"])

    args = arg_t([remote], [], False, False)

    # no packages present now
    assert len(spack.store.db.query()) == 0

    # have at least one package stacked (i.e. linked)
    assert spack.cmd.stack.stack(None, args) > 0

    # ignore already present symlinks
    args = arg_t([remote], [], True, False)

    # assert that another addition does not stack packages
    assert spack.cmd.stack.stack(None, args) == 0

    # packages present now in our db
    assert len(spack.store.db.query()) > 0
