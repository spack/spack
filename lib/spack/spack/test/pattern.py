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

import unittest

import spack.util.pattern as pattern


class CompositeTest(unittest.TestCase):

    def setUp(self):
        class Base:
            counter = 0

            def add(self):
                raise NotImplemented('add not implemented')

            def subtract(self):
                raise NotImplemented('subtract not implemented')

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

        self.Base = Base
        self.One = One
        self.Two = Two

    def test_composite_from_method_list(self):

        @pattern.composite(method_list=['add', 'subtract'])
        class CompositeFromMethodList:
            pass

        composite = CompositeFromMethodList()
        composite.append(self.One())
        composite.append(self.Two())
        composite.add()
        self.assertEqual(self.Base.counter, 3)
        composite.pop()
        composite.subtract()
        self.assertEqual(self.Base.counter, 2)

    def test_composite_from_interface(self):

        @pattern.composite(interface=self.Base)
        class CompositeFromInterface:
            pass

        composite = CompositeFromInterface()
        composite.append(self.One())
        composite.append(self.Two())
        composite.add()
        self.assertEqual(self.Base.counter, 3)
        composite.pop()
        composite.subtract()
        self.assertEqual(self.Base.counter, 2)

    def test_error_conditions(self):

        def wrong_container():
            @pattern.composite(interface=self.Base, container=2)
            class CompositeFromInterface:
                pass

        def no_methods():
            @pattern.composite()
            class CompositeFromInterface:
                pass

        self.assertRaises(TypeError, wrong_container)
        self.assertRaises(TypeError, no_methods)
