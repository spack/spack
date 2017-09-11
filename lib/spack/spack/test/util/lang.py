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

import llnl.util.lang


def test_owner_referencing():

    class A(object):

        def __init__(self):
            self.owner = None
            self.parent = None

    class B(object):

        a = llnl.util.lang.OwnerReferencing(
            name='_a', factory=A, owner_name='owner'
        )

    foo = B()

    assert foo.a.owner == foo
    assert foo.a.parent is None

    new_a = A()

    assert new_a.owner is None
    assert new_a.parent is None

    foo.a = new_a

    assert foo.a.owner == foo
    assert new_a.owner == foo
    assert foo.a.parent is None

    # Accessing through the class permits to tweak the descriptor
    B.a.owner_name = 'parent'
    foo.a = A()

    assert foo.a.owner is None
    assert foo.a.parent == foo
