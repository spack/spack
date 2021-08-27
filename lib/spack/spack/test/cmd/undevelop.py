# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.environment as ev
from spack.main import SpackCommand

undevelop = SpackCommand('undevelop')
env = SpackCommand('env')
concretize = SpackCommand('concretize')


def test_undevelop(tmpdir, config, mock_packages, mutable_mock_env_path):
    # setup environment
    with open(str(tmpdir.join('spack.yaml')), 'w') as f:
        f.write("""\
env:
  specs:
  - mpich@1.0

  develop:
  - spec: mpich
    path: /fake/path
""")

    with ev.Environment(str(tmpdir)) as e:
        e.concretize()
        before = e.matching_spec('mpich')
        undevelop('mpich')
        e.concretize()
        after = e.matching_spec('mpich')

    assert 'dev_path' in before.variants
    assert 'dev_path' not in after.variants


def test_undevelop_nonexistent(tmpdir, config, mock_packages, mutable_mock_env_path):
    # setup environment
    with open(str(tmpdir.join('spack.yaml')), 'w') as f:
        f.write("""\
env:
  specs:
  - mpich@1.0

  develop:
  - spec: mpich
    path: /fake/path
""")

    with ev.Environment(str(tmpdir)) as e:
        e.concretize()
        before = e.specs_by_hash
        undevelop('package-not-in-develop')  # does nothing
        e.concretize(force=True)
        after = e.specs_by_hash

    # nothing should have changed
    assert before == after
