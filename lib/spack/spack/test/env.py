# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Test environment internals without CLI"""
import filecmp
import os
import pickle
import sys

import pytest

import llnl.util.filesystem as fs

import spack.environment as ev
import spack.spec
from spack.environment.environment import SpackEnvironmentViewError, _error_on_nonempty_view_dir

pytestmark = pytest.mark.skipif(
    sys.platform == "win32", reason="Envs are not supported on windows"
)


class TestDirectoryInitialization:
    def test_environment_dir_from_name(self, mutable_mock_env_path):
        """Test the function mapping a managed environment name to its folder."""
        env = ev.create("test")
        environment_dir = ev.environment_dir_from_name("test")
        assert env.path == environment_dir
        with pytest.raises(ev.SpackEnvironmentError, match="environment already exists"):
            ev.environment_dir_from_name("test", exists_ok=False)


def test_hash_change_no_rehash_concrete(tmp_path, mock_packages, config):
    # create an environment
    env_path = tmp_path / "env_dir"
    env_path.mkdir(exist_ok=False)
    env = ev.create_in_dir(env_path)
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


def test_env_change_spec(tmp_path, mock_packages, config):
    env_path = tmp_path / "env_dir"
    env_path.mkdir(exist_ok=False)
    env = ev.create_in_dir(env_path)
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
spack:
  definitions:
  - compilers: ["%gcc", "%clang"]
  - desired_specs: ["mpileaks@2.1"]
  specs:
  - matrix:
    - [$compilers]
    - [$desired_specs]
"""


def test_env_change_spec_in_definition(tmp_path, mock_packages, config, mutable_mock_env_path):
    manifest_file = tmp_path / ev.manifest_name
    manifest_file.write_text(_test_matrix_yaml)
    e = ev.create("test", manifest_file)
    e.concretize()
    e.write()

    assert any(x.intersects("mpileaks@2.1%gcc") for x in e.user_specs)

    e.change_existing_spec(spack.spec.Spec("mpileaks@2.2"), list_name="desired_specs")
    e.write()

    assert any(x.intersects("mpileaks@2.2%gcc") for x in e.user_specs)
    assert not any(x.intersects("mpileaks@2.1%gcc") for x in e.user_specs)


def test_env_change_spec_in_matrix_raises_error(
    tmp_path, mock_packages, config, mutable_mock_env_path
):
    manifest_file = tmp_path / ev.manifest_name
    manifest_file.write_text(_test_matrix_yaml)
    e = ev.create("test", manifest_file)
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
        fst = ev.create_in_dir(env_path, with_view=view)
        fst.regenerate_views()

    # The view link should be created
    assert os.path.isdir(absolute_view)

    # Deserialize and check if the view path is still relative in yaml
    # and also check that the getter is pointing to the right dir.
    with fs.working_dir(str(tmpdir)):
        snd = ev.Environment(env_path)
        assert snd.manifest["spack"]["view"] == view
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


@pytest.mark.regression("35420")
@pytest.mark.parametrize(
    "original_content",
    [
        (
            """\
spack:
  specs:
  - matrix:
    # test
    - - a
  concretizer:
    unify: false"""
        )
    ],
)
def test_roundtrip_spack_yaml_with_comments(original_content, mock_packages, config, tmp_path):
    """Ensure that round-tripping a spack.yaml file doesn't change its content."""
    spack_yaml = tmp_path / "spack.yaml"
    spack_yaml.write_text(original_content)

    e = ev.Environment(tmp_path)
    e.manifest.flush()

    content = spack_yaml.read_text()
    assert content == original_content


def test_adding_anonymous_specs_to_env_fails(tmp_path):
    """Tests that trying to add an anonymous spec to the 'specs' section of an environment
    raises an exception
    """
    env = ev.create_in_dir(tmp_path)
    with pytest.raises(ev.SpackEnvironmentError, match="cannot add anonymous"):
        env.add("%gcc")


def test_removing_from_non_existing_list_fails(tmp_path):
    """Tests that trying to remove a spec from a non-existing definition fails."""
    env = ev.create_in_dir(tmp_path)
    with pytest.raises(ev.SpackEnvironmentError, match="'bar' does not exist"):
        env.remove("%gcc", list_name="bar")


@pytest.mark.parametrize(
    "init_view,update_value",
    [
        (True, False),
        (True, "./view"),
        (False, True),
        ("./view", True),
        ("./view", False),
        (True, True),
        (False, False),
    ],
)
def test_update_default_view(init_view, update_value, tmp_path, mock_packages, config):
    """Tests updating the default view with different values."""
    env = ev.create_in_dir(tmp_path, with_view=init_view)
    env.update_default_view(update_value)
    env.write(regenerate=True)
    if not isinstance(update_value, bool):
        assert env.default_view.raw_root == update_value

    expected_value = update_value
    if isinstance(init_view, str) and update_value is True:
        expected_value = init_view

    assert env.manifest.pristine_yaml_content["spack"]["view"] == expected_value


@pytest.mark.parametrize(
    "initial_content,update_value,expected_view",
    [
        (
            """
spack:
  specs:
  - mpileaks
  view:
    default:
      root: ./view-gcc
      select: ['%gcc']
      link_type: symlink
""",
            "./another-view",
            {"root": "./another-view", "select": ["%gcc"], "link_type": "symlink"},
        ),
        (
            """
spack:
  specs:
  - mpileaks
  view:
    default:
      root: ./view-gcc
      select: ['%gcc']
      link_type: symlink
""",
            True,
            {"root": "./view-gcc", "select": ["%gcc"], "link_type": "symlink"},
        ),
    ],
)
def test_update_default_complex_view(
    initial_content, update_value, expected_view, tmp_path, mock_packages, config
):
    spack_yaml = tmp_path / "spack.yaml"
    spack_yaml.write_text(initial_content)

    env = ev.Environment(tmp_path)
    env.update_default_view(update_value)
    env.write(regenerate=True)

    assert env.default_view.to_dict() == expected_view


@pytest.mark.parametrize("filename", [ev.manifest_name, ev.lockfile_name])
def test_cannot_initialize_in_dir_with_init_file(tmp_path, filename):
    """Tests that initializing an environment in a directory with an already existing
    spack.yaml or spack.lock raises an exception.
    """
    init_file = tmp_path / filename
    init_file.touch()
    with pytest.raises(ev.SpackEnvironmentError, match="cannot initialize"):
        ev.create_in_dir(tmp_path)


def test_cannot_initiliaze_if_dirname_exists_as_a_file(tmp_path):
    """Tests that initializing an environment using as a location an existing file raises
    an error.
    """
    dir_name = tmp_path / "dir"
    dir_name.touch()
    with pytest.raises(ev.SpackEnvironmentError, match="cannot initialize"):
        ev.create_in_dir(dir_name)


def test_cannot_initialize_if_init_file_does_not_exist(tmp_path):
    """Tests that initializing an environment passing a non-existing init file raises an error."""
    init_file = tmp_path / ev.manifest_name
    with pytest.raises(ev.SpackEnvironmentError, match="cannot initialize"):
        ev.create_in_dir(tmp_path, init_file=init_file)


def test_environment_pickle(tmp_path):
    env1 = ev.create_in_dir(tmp_path)
    obj = pickle.dumps(env1)
    env2 = pickle.loads(obj)
    assert isinstance(env2, ev.Environment)


def test_error_on_nonempty_view_dir(tmpdir):
    """Error when the target is not an empty dir"""
    with tmpdir.as_cwd():
        os.mkdir("empty_dir")
        os.mkdir("nonempty_dir")
        with open(os.path.join("nonempty_dir", "file"), "wb"):
            pass
        os.symlink("empty_dir", "symlinked_empty_dir")
        os.symlink("does_not_exist", "broken_link")
        os.symlink("broken_link", "file")

        # This is OK.
        _error_on_nonempty_view_dir("empty_dir")

        # This is not OK.
        with pytest.raises(SpackEnvironmentViewError):
            _error_on_nonempty_view_dir("nonempty_dir")

        with pytest.raises(SpackEnvironmentViewError):
            _error_on_nonempty_view_dir("symlinked_empty_dir")

        with pytest.raises(SpackEnvironmentViewError):
            _error_on_nonempty_view_dir("broken_link")

        with pytest.raises(SpackEnvironmentViewError):
            _error_on_nonempty_view_dir("file")


def test_can_add_specs_to_environment_without_specs_attribute(tmp_path, mock_packages, config):
    """Sometimes users have template manifest files, and save one line in the YAML file by
    removing the empty 'specs: []' attribute. This test ensures that adding a spec to an
    environment without the 'specs' attribute, creates the attribute first instead of returning
    an error.
    """
    spack_yaml = tmp_path / "spack.yaml"
    spack_yaml.write_text(
        """
spack:
  view: true
  concretizer:
    unify: true
    """
    )
    env = ev.Environment(tmp_path)
    env.add("a")

    assert len(env.user_specs) == 1
    assert env.manifest.pristine_yaml_content["spack"]["specs"] == ["a"]


@pytest.mark.parametrize(
    "original_yaml,new_spec,expected_yaml",
    [
        (
            """spack:
  specs:
  # baz
  - zlib
""",
            "libpng",
            """spack:
  specs:
  # baz
  - zlib
  - libpng
""",
        )
    ],
)
def test_preserving_comments_when_adding_specs(
    original_yaml, new_spec, expected_yaml, config, tmp_path
):
    """Ensure that round-tripping a spack.yaml file doesn't change its content."""
    spack_yaml = tmp_path / "spack.yaml"
    spack_yaml.write_text(original_yaml)

    e = ev.Environment(str(tmp_path))
    e.add(new_spec)
    e.write()

    content = spack_yaml.read_text()
    assert content == expected_yaml


@pytest.mark.parametrize("filename", [ev.lockfile_name, "as9582g54.lock", "m3ia54s.json"])
@pytest.mark.regression("37410")
def test_initialize_from_lockfile(tmp_path, filename):
    """Some users have workflows where they store multiple lockfiles in the
    same directory, and pick one of them to create an environment depending
    on external parameters e.g. while running CI jobs. This test ensures that
    Spack can create environments from lockfiles that are not necessarily named
    'spack.lock' and can thus coexist in the same directory.
    """

    init_file = tmp_path / filename
    env_dir = tmp_path / "env_dir"
    init_file.write_text('{ "roots": [] }\n')
    ev.initialize_environment_dir(env_dir, init_file)

    assert os.path.exists(env_dir / ev.lockfile_name)
    assert filecmp.cmp(env_dir / ev.lockfile_name, init_file, shallow=False)


def test_cannot_initialize_from_bad_lockfile(tmp_path):
    """Test that we fail on an incorrectly constructed lockfile"""

    init_file = tmp_path / ev.lockfile_name
    env_dir = tmp_path / "env_dir"

    init_file.write_text("Not a legal JSON file\n")

    with pytest.raises(ev.SpackEnvironmentError, match="from lockfile"):
        ev.initialize_environment_dir(env_dir, init_file)


@pytest.mark.parametrize("filename", ["random.txt", "random.yaml", ev.manifest_name])
@pytest.mark.regression("37410")
def test_initialize_from_random_file_as_manifest(tmp_path, filename):
    """Some users have workflows where they store multiple lockfiles in the
    same directory, and pick one of them to create an environment depending
    on external parameters e.g. while running CI jobs. This test ensures that
    Spack can create environments from manifest that are not necessarily named
    'spack.yaml' and can thus coexist in the same directory.
    """

    init_file = tmp_path / filename
    env_dir = tmp_path / "env_dir"

    init_file.write_text(
        """\
spack:
  view: true
  concretizer:
    unify: true
  specs: []
"""
    )

    ev.create_in_dir(env_dir, init_file)

    assert not os.path.exists(env_dir / ev.lockfile_name)
    assert os.path.exists(env_dir / ev.manifest_name)
    assert filecmp.cmp(env_dir / ev.manifest_name, init_file, shallow=False)


def test_error_message_when_using_too_new_lockfile(tmp_path):
    """Sometimes the lockfile format needs to be bumped. When that happens, we have forward
    incompatibilities that need to be reported in a clear way to the user, in case we moved
    back to an older version of Spack. This test ensures that the error message for a too
    new lockfile version stays comprehensible across refactoring of the environment code.
    """
    init_file = tmp_path / ev.lockfile_name
    env_dir = tmp_path / "env_dir"
    init_file.write_text(
        """
{
    "_meta": {
        "file-type": "spack-lockfile",
        "lockfile-version": 100,
        "specfile-version": 3
    },
    "roots": [],
    "concrete_specs": {}
}\n
"""
    )
    ev.initialize_environment_dir(env_dir, init_file)
    with pytest.raises(ev.SpackEnvironmentError, match="You need to use a newer Spack version."):
        ev.Environment(env_dir)


@pytest.mark.regression("38240")
@pytest.mark.parametrize(
    "unify_in_lower_scope,unify_in_spack_yaml",
    [
        (True, False),
        (True, "when_possible"),
        (False, True),
        (False, "when_possible"),
        ("when_possible", False),
        ("when_possible", True),
    ],
)
def test_environment_concretizer_scheme_used(tmp_path, unify_in_lower_scope, unify_in_spack_yaml):
    """Tests that "unify" settings in spack.yaml always take precedence over settings in lower
    configuration scopes.
    """
    manifest = tmp_path / "spack.yaml"
    manifest.write_text(
        f"""\
spack:
  specs:
  - mpileaks
  concretizer:
    unify: {str(unify_in_spack_yaml).lower()}
"""
    )

    with spack.config.override("concretizer:unify", unify_in_lower_scope):
        with ev.Environment(manifest.parent) as e:
            assert e.unify == unify_in_spack_yaml


@pytest.mark.parametrize("unify_in_config", [True, False, "when_possible"])
def test_environment_config_scheme_used(tmp_path, unify_in_config):
    """Tests that "unify" settings in lower configuration scopes is taken into account,
    if absent in spack.yaml.
    """
    manifest = tmp_path / "spack.yaml"
    manifest.write_text(
        """\
spack:
  specs:
  - mpileaks
"""
    )

    with spack.config.override("concretizer:unify", unify_in_config):
        with ev.Environment(manifest.parent) as e:
            assert e.unify == unify_in_config


@pytest.mark.parametrize(
    "spec_str,expected_raise,expected_spec",
    [
        # vendorsb vendors "b" only when @=1.1
        ("vendorsb", False, "vendorsb@=1.0"),
        ("vendorsb@=1.1", True, None),
    ],
)
def test_vendors_directive(
    spec_str, expected_raise, expected_spec, tmp_path, mock_packages, config
):
    """Tests that we cannot concretize two specs together, if one vendors the other."""
    if spack.config.get("config:concretizer") == "original":
        pytest.xfail("Known failure of the original concretizer")

    manifest = tmp_path / "spack.yaml"
    manifest.write_text(
        f"""\
spack:
  specs:
  - {spec_str}
  - b
  concretizer:
    unify: true
"""
    )
    with ev.Environment(manifest.parent) as e:
        if expected_raise:
            with pytest.raises(spack.solver.asp.UnsatisfiableSpecError):
                e.concretize()
        else:
            e.concretize()
            assert any(s.satisfies(expected_spec) for s in e.concrete_roots())
