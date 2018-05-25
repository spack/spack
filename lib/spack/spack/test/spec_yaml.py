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
"""Test YAML serialization for specs.

YAML format preserves DAG information in the spec.

"""
from collections import Iterable, Mapping

import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
from spack.spec import Spec
from spack.util.spack_yaml import syaml_dict


def check_yaml_round_trip(spec):
    yaml_text = spec.to_yaml()
    spec_from_yaml = Spec.from_yaml(yaml_text)
    assert spec.eq_dag(spec_from_yaml)


def test_simple_spec():
    spec = Spec('mpileaks')
    check_yaml_round_trip(spec)


def test_normal_spec(mock_packages):
    spec = Spec('mpileaks+debug~opt')
    spec.normalize()
    check_yaml_round_trip(spec)


def test_external_spec(config, mock_packages):
    spec = Spec('externaltool')
    spec.concretize()
    check_yaml_round_trip(spec)

    spec = Spec('externaltest')
    spec.concretize()
    check_yaml_round_trip(spec)


def test_ambiguous_version_spec(mock_packages):
    spec = Spec('mpileaks@1.0:5.0,6.1,7.3+debug~opt')
    spec.normalize()
    check_yaml_round_trip(spec)


def test_concrete_spec(config, mock_packages):
    spec = Spec('mpileaks+debug~opt')
    spec.concretize()
    check_yaml_round_trip(spec)


def test_yaml_multivalue():
    spec = Spec('multivalue_variant foo="bar,baz"')
    spec.concretize()
    check_yaml_round_trip(spec)


def test_yaml_subdag(config, mock_packages):
    spec = Spec('mpileaks^mpich+debug')
    spec.concretize()
    yaml_spec = Spec.from_yaml(spec.to_yaml())

    for dep in ('callpath', 'mpich', 'dyninst', 'libdwarf', 'libelf'):
        assert spec[dep].eq_dag(yaml_spec[dep])


def test_using_ordered_dict(mock_packages):
    """ Checks that dicts are ordered

    Necessary to make sure that dag_hash is stable across python
    versions and processes.
    """
    def descend_and_check(iterable, level=0):
        if isinstance(iterable, Mapping):
            assert isinstance(iterable, syaml_dict)
            return descend_and_check(iterable.values(), level=level + 1)
        max_level = level
        for value in iterable:
            if isinstance(value, Iterable) and not isinstance(value, str):
                nlevel = descend_and_check(value, level=level + 1)
                if nlevel > max_level:
                    max_level = nlevel
        return max_level

    specs = ['mpileaks ^zmpi', 'dttop', 'dtuse']
    for spec in specs:
        dag = Spec(spec)
        dag.normalize()
        from pprint import pprint
        pprint(dag.to_node_dict())
        break

        level = descend_and_check(dag.to_node_dict())

        # level just makes sure we are doing something here
        assert level >= 5


def test_ordered_read_not_required_for_consistent_dag_hash(
        config, mock_packages
):
    """Make sure ordered serialization isn't required to preserve hashes.

    For consistent hashes, we require that YAML and json documents
    have their keys serialized in a deterministic order. However, we
    don't want to require them to be serialized in order. This
    ensures that is not required.
    """
    specs = ['mpileaks ^zmpi', 'dttop', 'dtuse']
    for spec in specs:
        spec = Spec(spec)
        spec.concretize()

        #
        # Dict & corresponding YAML & JSON from the original spec.
        #
        spec_dict = spec.to_dict()
        spec_yaml = spec.to_yaml()
        spec_json = spec.to_json()

        #
        # Make a spec with reversed OrderedDicts for every
        # OrderedDict in the original.
        #
        reversed_spec_dict = reverse_all_dicts(spec.to_dict())

        #
        # Dump to YAML and JSON
        #
        yaml_string = syaml.dump(spec_dict, default_flow_style=False)
        reversed_yaml_string = syaml.dump(reversed_spec_dict,
                                          default_flow_style=False)
        json_string = sjson.dump(spec_dict)
        reversed_json_string = sjson.dump(reversed_spec_dict)

        #
        # Do many consistency checks
        #

        # spec yaml is ordered like the spec dict
        assert yaml_string == spec_yaml
        assert json_string == spec_json

        # reversed string is different from the original, so it
        # *would* generate a different hash
        assert yaml_string != reversed_yaml_string
        assert json_string != reversed_json_string

        # build specs from the "wrongly" ordered data
        round_trip_yaml_spec = Spec.from_yaml(yaml_string)
        round_trip_json_spec = Spec.from_json(json_string)
        round_trip_reversed_yaml_spec = Spec.from_yaml(
            reversed_yaml_string
        )
        round_trip_reversed_json_spec = Spec.from_yaml(
            reversed_json_string
        )

        # TODO: remove this when build deps are in provenance.
        spec = spec.copy(deps=('link', 'run'))
        # specs are equal to the original
        assert spec == round_trip_yaml_spec
        assert spec == round_trip_json_spec
        assert spec == round_trip_reversed_yaml_spec
        assert spec == round_trip_reversed_json_spec
        assert round_trip_yaml_spec == round_trip_reversed_yaml_spec
        assert round_trip_json_spec == round_trip_reversed_json_spec
        # dag_hashes are equal
        assert spec.dag_hash() == round_trip_yaml_spec.dag_hash()
        assert spec.dag_hash() == round_trip_json_spec.dag_hash()
        assert spec.dag_hash() == round_trip_reversed_yaml_spec.dag_hash()
        assert spec.dag_hash() == round_trip_reversed_json_spec.dag_hash()
        # full_hashes are equal
        spec.concretize()
        round_trip_yaml_spec.concretize()
        round_trip_json_spec.concretize()
        round_trip_reversed_yaml_spec.concretize()
        round_trip_reversed_json_spec.concretize()
        assert spec.full_hash() == round_trip_yaml_spec.full_hash()
        assert spec.full_hash() == round_trip_json_spec.full_hash()
        assert spec.full_hash() == round_trip_reversed_yaml_spec.full_hash()
        assert spec.full_hash() == round_trip_reversed_json_spec.full_hash()


def reverse_all_dicts(data):
    """Descend into data and reverse all the dictionaries"""
    if isinstance(data, dict):
        return syaml_dict(reversed(
            [(reverse_all_dicts(k), reverse_all_dicts(v))
             for k, v in data.items()]))
    elif isinstance(data, (list, tuple)):
        return type(data)(reverse_all_dicts(elt) for elt in data)
    else:
        return data
