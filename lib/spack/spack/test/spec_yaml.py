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
"""Test YAML serialization for specs.

YAML format preserves DAG informatoin in the spec.

"""
from spack.spec import Spec
from spack.test.mock_packages_test import *

class SpecDagTest(MockPackagesTest):

    def check_yaml_round_trip(self, spec):
        yaml_text = spec.to_yaml()
        spec_from_yaml = Spec.from_yaml(yaml_text)
        self.assertTrue(spec.eq_dag(spec_from_yaml))


    def test_simple_spec(self):
        spec = Spec('mpileaks')
        self.check_yaml_round_trip(spec)


    def test_normal_spec(self):
        spec = Spec('mpileaks+debug~opt')
        spec.normalize()
        self.check_yaml_round_trip(spec)


    def test_ambiguous_version_spec(self):
        spec = Spec('mpileaks@1.0:5.0,6.1,7.3+debug~opt')
        spec.normalize()
        self.check_yaml_round_trip(spec)


    def test_concrete_spec(self):
        spec = Spec('mpileaks+debug~opt')
        spec.concretize()
        self.check_yaml_round_trip(spec)


    def test_yaml_subdag(self):
        spec = Spec('mpileaks^mpich+debug')
        spec.concretize()

        yaml_spec = Spec.from_yaml(spec.to_yaml())

        for dep in ('callpath', 'mpich', 'dyninst', 'libdwarf', 'libelf'):
            self.assertTrue(spec[dep].eq_dag(yaml_spec[dep]))
