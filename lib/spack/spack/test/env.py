# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Test environment internals without CLI"""
import io
import os
import sys

import pytest

import llnl.util.filesystem as fs

import spack.environment as ev
import spack.spec

pytestmark = pytest.mark.skipif(
    sys.platform == "win32", reason="Envs are not supported on windows"
)


def test_hash_change_no_rehash_concrete(tmpdir, mock_packages, config):
    # create an environment
    env_path = tmpdir.mkdir("env_dir").strpath
    env = ev.Environment(env_path)
    env.write()

    # add a spec with a rewritten build hash
    spec = spack.spec.Spec("mpileaks")
    env.add(spec)
    env.concretize()

    # rewrite the hash
    old_hash = env.concretized_order[0]
    new_hash = "abc"
    env.specs_by_hash[old_hash]._hash = new_hash
    env.concretized_order[0] = new_hash
    env.specs_by_hash[new_hash] = env.specs_by_hash[old_hash]
    del env.specs_by_hash[old_hash]
    env.write()

    # Read environment
    read_in = ev.Environment(env_path)

    # Ensure read hashes are used (rewritten hash seen on read)
    assert read_in.concretized_order
    assert read_in.concretized_order[0] in read_in.specs_by_hash
    assert read_in.specs_by_hash[read_in.concretized_order[0]]._hash == new_hash


def test_env_change_spec(tmpdir, mock_packages, config):
    env_path = tmpdir.mkdir("env_dir").strpath
    env = ev.Environment(env_path)
    env.write()

    spec = spack.spec.Spec("mpileaks@2.1~shared+debug")
    env.add(spec)
    env.write()

    change_spec = spack.spec.Spec("mpileaks@2.2")
    env.change_existing_spec(change_spec)
    (spec,) = env.added_specs()
    assert spec == spack.spec.Spec("mpileaks@2.2~shared+debug")

    change_spec = spack.spec.Spec("mpileaks~debug")
    env.change_existing_spec(change_spec)
    (spec,) = env.added_specs()
    assert spec == spack.spec.Spec("mpileaks@2.2~shared~debug")


_test_matrix_yaml = """\
env:
  definitions:
  - compilers: ["%gcc", "%clang"]
  - desired_specs: ["mpileaks@2.1"]
  specs:
  - matrix:
    - [$compilers]
    - [$desired_specs]
"""


def test_env_change_spec_in_definition(tmpdir, mock_packages, config, mutable_mock_env_path):
    initial_yaml = io.StringIO(_test_matrix_yaml)
    e = ev.create("test", initial_yaml)
    e.concretize()
    e.write()

    assert any(x.intersects("mpileaks@2.1%gcc") for x in e.user_specs)

    e.change_existing_spec(spack.spec.Spec("mpileaks@2.2"), list_name="desired_specs")
    e.write()

    assert any(x.intersects("mpileaks@2.2%gcc") for x in e.user_specs)
    assert not any(x.intersects("mpileaks@2.1%gcc") for x in e.user_specs)


def test_env_change_spec_in_matrix_raises_error(
    tmpdir, mock_packages, config, mutable_mock_env_path
):
    initial_yaml = io.StringIO(_test_matrix_yaml)
    e = ev.create("test", initial_yaml)
    e.concretize()
    e.write()

    with pytest.raises(spack.environment.SpackEnvironmentError) as error:
        e.change_existing_spec(spack.spec.Spec("mpileaks@2.2"))
    assert "Cannot directly change specs in matrices" in str(error)


def test_activate_should_require_an_env():
    with pytest.raises(TypeError):
        ev.activate(env="name")

    with pytest.raises(TypeError):
        ev.activate(env=None)


def test_user_view_path_is_not_canonicalized_in_yaml(tmpdir, config):
    # When spack.yaml files are checked into version control, we
    # don't want view: ./relative to get canonicalized on disk.

    # We create a view in <tmpdir>/env_dir
    env_path = tmpdir.mkdir("env_dir").strpath

    # And use a relative path to specify the view dir
    view = os.path.join(".", "view")

    # Which should always resolve to the following independent of cwd.
    absolute_view = os.path.join(env_path, "view")

    # Serialize environment with relative view path
    with fs.working_dir(str(tmpdir)):
        fst = ev.Environment(env_path, with_view=view)
        fst.write()

    # The view link should be created
    assert os.path.isdir(absolute_view)

    # Deserialize and check if the view path is still relative in yaml
    # and also check that the getter is pointing to the right dir.
    with fs.working_dir(str(tmpdir)):
        snd = ev.Environment(env_path)
        assert snd.yaml["spack"]["view"] == view
        assert os.path.samefile(snd.default_view.root, absolute_view)


def test_environment_cant_modify_environments_root(tmpdir):
    filename = str(tmpdir.join("spack.yaml"))
    with open(filename, "w") as f:
        f.write(
            """\
 spack:
   config:
     environments_root: /a/black/hole
   view: false
   specs: []
 """
        )
    with tmpdir.as_cwd():
        with pytest.raises(ev.SpackEnvironmentError):
            e = ev.Environment(tmpdir.strpath)
            ev.activate(e)
