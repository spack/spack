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

import pytest

from spack.util.pattern import composite


class Base(object):
    counter = 0

    @classmethod
    def reset(cls):
        cls.counter = 0

    def add(self):
        raise NotImplemented('add not implemented')

    def subtract(self):
        raise NotImplemented('subtract not implemented')

    @staticmethod
    def get_number():
        return Base.counter


class One(Base):
    def add(self):
        Base.counter += 1

    def subtract(self):
        Base.counter -= 1


class Two(Base):
    def add(self):
        Base.counter += 2

    def subtract(self):
        Base.counter -= 2


@pytest.fixture
def composite_items():
    Base.reset()  # Make sure that the initial state is always consistent
    one = One()
    two = Two()
    return one, two


class TestCompositeUsage:
    def test_composite_from_method_list(self, composite_items):
        @composite(method_list=['add', 'subtract'])
        class CompositeFromMethodList(object):
            @staticmethod
            def get_number():
                return 0

        one, two = composite_items

        composite_object = CompositeFromMethodList()
        composite_object.append(one)
        composite_object.append(two)
        composite_object.add()
        assert Base.counter == 3

        composite_object.pop()
        composite_object.subtract()
        assert Base.counter == 2

        assert CompositeFromMethodList.get_number() == 0

    def test_composite_from_interface(self, composite_items):
        @composite(interface=Base)
        class CompositeFromInterface(object):
            pass

        one, two = composite_items

        composite_object = CompositeFromInterface()

        composite_object.append(one)
        composite_object.append(two)
        composite_object.add()
        assert Base.counter == 3

        composite_object.pop()
        composite_object.subtract()
        assert Base.counter == 2

        assert CompositeFromInterface.get_number() == 2
        assert isinstance(composite_object, Base)
        assert issubclass(CompositeFromInterface, Base)

    def test_get_item(self, composite_items):
        @composite(interface=Base)
        class CompositeFromInterface(object):
            pass

        one, two = composite_items
        composite_object = CompositeFromInterface()

        composite_object.append(one, 'one')
        composite_object.append(two, 'two')

        # Check indexed access
        assert composite_object[0] is one
        assert composite_object[1] is two

        # Check access by name
        assert composite_object['one'] is one
        assert composite_object['two'] is two

        # Check contains
        assert one in composite_object
        assert two in composite_object
        assert 'one' in composite_object
        assert 'two' in composite_object

        # Check assignment
        composite_object[:] = [two, one]

        assert composite_object[0] is two
        assert composite_object[1] is one
        assert composite_object['one'] is one
        assert composite_object['two'] is two

        composite_object[:] = [two, two]

        assert composite_object[0] is two
        assert composite_object[1] is two
        assert 'one' not in composite_object
        assert composite_object['two'] is two

        # Check deletion

        assert len(composite_object) == 2

        del composite_object[0]

        assert len(composite_object) == 1
        assert composite_object[0] == two
        assert 'two' in composite_object

        del composite_object[0]

        assert len(composite_object) == 0
        assert 'two' not in composite_object


class TestCompositeFailures:
    def test_wrong_container(self):
        with pytest.raises(TypeError):

            @composite(interface=Base, container=2)
            class CompositeFromInterface:
                pass

    def test_no_interface_given(self):
        with pytest.raises(TypeError):

            @composite()
            class CompositeFromInterface:
                pass


class BaseReduction(object):
    def get_int(self):
        pass

    def get_string(self):
        pass


class A(BaseReduction):
    def get_int(self):
        return 10

    def get_string(self):
        return 'Hello '


class B(BaseReduction):
    def get_int(self):
        return 11

    def get_string(self):
        return 'world!'


@pytest.fixture
def composite_reduction_items():
    a = A()
    b = B()
    return a, b


class TestCompositeReduction:
    def test_reduction(self, composite_reduction_items):
        class Multiplier(object):
            def __init__(self):
                self.value = 1

            def __call__(self, value):
                self.value *= value
                return self.value

        class Adder(object):
            def __init__(self):
                self.value = ''

            def __call__(self, value):
                self.value += value
                return self.value

        adder, multiplier = Adder(), Multiplier()

        @composite(
            interface=BaseReduction,
            reductions={'get_int': multiplier, 'get_string': adder}
        )
        class CompositeReduction(object):
            pass

        composite_object = CompositeReduction()
        composite_object.extend(composite_reduction_items)

        assert composite_object.get_int() == 110
        assert composite_object.get_string() == 'Hello world!'

    def test_wrong_reduction_type(self):
        with pytest.raises(TypeError):

            @composite(interface=BaseReduction, reductions=[])
            class CompositeReductionInterface(object):
                pass
