# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest

import spack
import spack.environment as ev
from spack import repo
from spack.cmd.release_jobs import stage_spec_jobs, spec_deps_key_label
from spack.main import SpackCommand
from spack.spec import Spec
from spack.test.conftest import MockPackage, MockPackageMultiRepo


env = SpackCommand('env')
release_jobs = SpackCommand('release-jobs')


@pytest.fixture()
def env_deactivate():
    yield
    spack.environment._active_environment = None
    os.environ.pop('SPACK_ENV', None)


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
        spec_a = Spec('a')
        spec_a.concretize()

        spec_a_label = spec_deps_key_label(spec_a)[1]
        spec_b_label = spec_deps_key_label(spec_a['b'])[1]
        spec_c_label = spec_deps_key_label(spec_a['c'])[1]
        spec_d_label = spec_deps_key_label(spec_a['d'])[1]
        spec_e_label = spec_deps_key_label(spec_a['e'])[1]
        spec_f_label = spec_deps_key_label(spec_a['f'])[1]
        spec_g_label = spec_deps_key_label(spec_a['g'])[1]

        spec_labels, dependencies, stages = stage_spec_jobs([spec_a])

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


def test_release_jobs_with_env(tmpdir, mutable_mock_env_path, env_deactivate,
                               install_mockery, mock_packages):
    """Make sure we can get a .gitlab-ci.yml from an environment file
    which has the gitlab-ci, cdash, and mirrors sections."""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  definitions:
    - packages: [archive-files]
  specs:
    - $packages
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    mappings:
      - match:
          - archive-files
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
  cdash:
    build-group: Not important
    url: https://my.fake.cdash
    project: Not used
    site: Nothing
""")
    with tmpdir.as_cwd():
        env('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            release_jobs('--output-file', outputfile)

        with open(outputfile) as f:
            contents = f.read()
            assert('archive-files' in contents)
            assert('stages: [stage-0' in contents)
