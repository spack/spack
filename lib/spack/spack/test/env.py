# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test environment internals without CLI"""

import pytest

import spack.environment as ev
import spack.spec


@pytest.mark.skipif(str(spack.platforms.host()) == 'windows',
                    reason='Not supported on Windows (yet)')
def test_hash_change_no_rehash_concrete(tmpdir, mock_packages, config):
    # create an environment
    env_path = tmpdir.mkdir('env_dir').strpath
    env = ev.Environment(env_path)
    env.write()

    # add a spec with a rewritten build hash
    spec = spack.spec.Spec('mpileaks')
    env.add(spec)
    env.concretize()

    # rewrite the hash
    old_hash = env.concretized_order[0]
    new_hash = 'abc'
    env.specs_by_hash[old_hash]._build_hash = new_hash
    env.concretized_order[0] = new_hash
    env.specs_by_hash[new_hash] = env.specs_by_hash[old_hash]
    del env.specs_by_hash[old_hash]
    env.write()

    # Read environment
    read_in = ev.Environment(env_path)

    # Ensure read hashes are used (rewritten hash seen on read)
    assert read_in.concretized_order
    assert read_in.concretized_order[0] in read_in.specs_by_hash
    assert read_in.specs_by_hash[read_in.concretized_order[0]]._build_hash == new_hash


def test_activate_should_require_an_env():
    with pytest.raises(TypeError):
        ev.activate(env='name')

    with pytest.raises(TypeError):
        ev.activate(env=None)
