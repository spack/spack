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
import spack.util.pattern as pattern


@pytest.fixture()
def interface():
    """Returns the interface class for the composite."""
    class Base:
        counter = 0

        def add(self):
            raise NotImplemented('add not implemented')

        def subtract(self):
            raise NotImplemented('subtract not implemented')

    return Base


@pytest.fixture()
def implementation(interface):
    """Returns an implementation of the interface"""
    class Implementation(interface):

            def __init__(self, value):
                self.value = value

            def add(self):
                interface.counter += self.value

            def subtract(self):
                interface.counter -= self.value

    return Implementation


@pytest.fixture(params=[
    'interface',
    'method_list'
])
def composite(interface, implementation, request):
    """Returns a composite that contains an instance of `implementation(1)`
    and one of `implementation(2)`.
    """
    if request.param == 'interface':
        @pattern.composite(interface=interface)
        class Composite:
            pass

    else:
        @pattern.composite(method_list=['add', 'subtract'])
        class Composite:
            pass

    c = Composite()
    c.append(implementation(1))
    c.append(implementation(2))

    return c


def test_composite_interface_calls(interface, composite):

    composite.add()
    assert interface.counter == 3

    composite.pop()
    composite.subtract()
    assert interface.counter == 2


def test_composite_wrong_container(interface):

    with pytest.raises(TypeError):
        @pattern.composite(interface=interface, container=2)
        class CompositeFromInterface:
            pass


def test_composite_no_methods():

    with pytest.raises(TypeError):
        @pattern.composite()
        class CompositeFromInterface:
            pass
