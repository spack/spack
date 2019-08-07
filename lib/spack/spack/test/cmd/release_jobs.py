# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import json
import sys

from jsonschema import validate

from spack import repo
from spack.architecture import sys_type
from spack.cmd.release_jobs import stage_spec_jobs, spec_deps_key_label
from spack.main import SpackCommand
from spack.schema.specs_deps import schema as specs_deps_schema
from spack.spec import Spec
from spack.test.conftest import MockPackage, MockPackageMultiRepo


release_jobs = SpackCommand('release-jobs')


def test_specs_deps(tmpdir, config):
    """If we ask for the specs dependencies to be written to disk, then make
    sure we get a file of the correct format."""

    output_path = str(tmpdir.mkdir('json').join('spec_deps.json'))
    release_jobs('--specs-deps-output', output_path, 'readline')

    deps_object = None

    with open(output_path, 'r') as fd:
        deps_object = json.loads(fd.read())

    assert (deps_object is not None)

    validate(deps_object, specs_deps_schema)


@pytest.mark.skipif(
    sys.version_info[:2] < (2, 7),
    reason="For some reason in Python2.6 we get a utf-32 string "
           "that can't be parsed"
)
def test_specs_staging(config):
    """Make sure we achieve the best possible staging for the following
spec DAG::

        a
       /|
      c b
        |\
        e d
          |\
          f g

In this case, we would expect 'c', 'e', 'f', and 'g' to be in the first stage,
and then 'd', 'b', and 'a' to be put in the next three stages, respectively.

"""
    current_system = sys_type()

    config_compilers = config.get_config('compilers')
    first_compiler = config_compilers[0]
    compiler_spec = first_compiler['compiler']['spec']

    # Whatever that first compiler in the configuration was, let's make sure
    # we mock up an entry like we'd find in os-container-mapping.yaml which
    # has that compiler.
    mock_containers = {}
    mock_containers[current_system] = {
        "image": "dontcare",
        "compilers": [
            {
                "name": compiler_spec,
            }
        ],
    }

    default = ('build', 'link')

    g = MockPackage('g', [], [])
    f = MockPackage('f', [], [])
    e = MockPackage('e', [], [])
    d = MockPackage('d', [f, g], [default, default])
    c = MockPackage('c', [], [])
    b = MockPackage('b', [d, e], [default, default])
    a = MockPackage('a', [b, c], [default, default])

    mock_repo = MockPackageMultiRepo([a, b, c, d, e, f, g])

    with repo.swap(mock_repo):
        # Now we'll ask for the root package to be compiled with whatever that
        # first compiler in the configuration was.
        spec_a = Spec('a%{0}'.format(compiler_spec))
        spec_a.concretize()

        spec_a_label = spec_deps_key_label(spec_a)[1]
        spec_b_label = spec_deps_key_label(spec_a['b'])[1]
        spec_c_label = spec_deps_key_label(spec_a['c'])[1]
        spec_d_label = spec_deps_key_label(spec_a['d'])[1]
        spec_e_label = spec_deps_key_label(spec_a['e'])[1]
        spec_f_label = spec_deps_key_label(spec_a['f'])[1]
        spec_g_label = spec_deps_key_label(spec_a['g'])[1]

        spec_labels, dependencies, stages = stage_spec_jobs(
            [spec_a], mock_containers, current_system)

        assert (len(stages) == 4)

        assert (len(stages[0]) == 4)
        assert (spec_c_label in stages[0])
        assert (spec_e_label in stages[0])
        assert (spec_f_label in stages[0])
        assert (spec_g_label in stages[0])

        assert (len(stages[1]) == 1)
        assert (spec_d_label in stages[1])

        assert (len(stages[2]) == 1)
        assert (spec_b_label in stages[2])

        assert (len(stages[3]) == 1)
        assert (spec_a_label in stages[3])
