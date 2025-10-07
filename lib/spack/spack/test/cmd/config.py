# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import functools
import json
import os
import pathlib
import re

import pytest

import spack.concretize
import spack.config
import spack.database
import spack.environment as ev
import spack.llnl.util.filesystem as fs
import spack.main
import spack.schema.config
import spack.store
import spack.util.spack_yaml as syaml

config = spack.main.SpackCommand("config")
env = spack.main.SpackCommand("env")

pytestmark = pytest.mark.usefixtures("mock_packages")


def _create_config(scope=None, data={}, section="packages"):
    scope = scope or spack.config.default_modify_scope()
    cfg_file = spack.config.CONFIG.get_config_filename(scope, section)
    with open(cfg_file, "w", encoding="utf-8") as f:
        syaml.dump(data, stream=f)
    return cfg_file


@pytest.fixture()
def config_yaml_v015(mutable_config):
    """Create a packages.yaml in the old format"""
    old_data = {
        "config": {"install_tree": "/fake/path", "install_path_scheme": "{name}-{version}"}
    }
    return functools.partial(_create_config, data=old_data, section="config")


scope_path_re = r"\(([^\)]+)\)"


@pytest.mark.parametrize(
    "path,types",
    [
        (False, []),
        (True, []),
        (False, ["path"]),
        (False, ["env"]),
        (False, ["internal", "include"]),
    ],
)
def test_config_scopes(path, types, mutable_mock_env_path):
    ev.create("test")
    scopes_cmd = ["scopes"]
    if path:
        scopes_cmd.append("-p")
    if types:
        scopes_cmd.extend(["-t", *types])
    output = config(*scopes_cmd).split()
    if not types or any(i in ("all", "internal") for i in types):
        assert "command_line" in output
        assert "_builtin" in output
    if types:
        if not any(i in ("all", "path") for i in types):
            assert "site" not in output
        if not any(i in ("all", "env", "include", "path") for i in types):
            assert not output or all(":" not in x for x in output)
        if not any(i in ("all", "env", "path") for i in types):
            assert not output or all(not x.startswith("env:") for x in output)
        if not any(i in ("all", "internal") for i in types):
            assert "command_line" not in output
            assert "_builtin" not in output
    if path:
        paths = (x[1] for x in (re.fullmatch(scope_path_re, s) for s in output) if x)
        assert all(os.sep in x for x in paths)


def test_config_scopes_include():
    scopes_cmd = ["scopes", "-t", "include"]
    output = config(*scopes_cmd).split()
    assert not output or all(":" in x for x in output)


def test_config_scopes_path_section():
    output = config("scopes", "-t", "include", "-p", "modules")
    assert "_builtin" not in output
    assert "site" not in output


def test_get_config_scope(mock_low_high_config):
    assert config("get", "compilers").strip() == "compilers: {}"


def test_get_config_roundtrip(mutable_config):
    """Test that ``spack config get [--json] <section>`` roundtrips correctly."""
    json_roundtrip = json.loads(config("get", "--json", "config"))
    yaml_roundtrip = syaml.load(config("get", "config"))
    assert json_roundtrip["config"] == yaml_roundtrip["config"] == mutable_config.get("config")


def test_get_all_config_roundtrip(mutable_config):
    """Test that ``spack config get [--json]`` roundtrips correctly."""
    json_roundtrip = json.loads(config("get", "--json"))
    yaml_roundtrip = syaml.load(config("get"))
    assert json_roundtrip == yaml_roundtrip
    for section in spack.config.SECTION_SCHEMAS:
        assert json_roundtrip["spack"][section] == mutable_config.get(section)


def test_get_config_scope_merged(mock_low_high_config):
    low_path = mock_low_high_config.scopes["low"].path
    high_path = mock_low_high_config.scopes["high"].path

    fs.mkdirp(low_path)
    fs.mkdirp(high_path)

    with open(os.path.join(low_path, "repos.yaml"), "w", encoding="utf-8") as f:
        f.write(
            """\
repos:
  repo3: repo3
"""
        )

    with open(os.path.join(high_path, "repos.yaml"), "w", encoding="utf-8") as f:
        f.write(
            """\
repos:
  repo1: repo1
  repo2: repo2
"""
        )

    assert (
        config("get", "repos").strip()
        == """repos:
  repo1: repo1
  repo2: repo2
  repo3: repo3"""
    )


def test_config_edit(mutable_config, working_env):
    """Ensure `spack config edit` edits the right paths."""

    dms = spack.config.default_modify_scope("compilers")
    dms_path = spack.config.CONFIG.scopes[dms].path
    user_path = spack.config.CONFIG.scopes["user"].path

    comp_path = os.path.join(dms_path, "compilers.yaml")
    repos_path = os.path.join(user_path, "repos.yaml")

    assert config("edit", "--print-file", "compilers").strip() == comp_path
    assert config("edit", "--print-file", "repos").strip() == repos_path


def test_config_get_gets_spack_yaml(mutable_mock_env_path):
    with ev.create("test") as env:
        assert "mpileaks" not in config("get")
        env.add("mpileaks")
        env.write()
        assert "mpileaks" in config("get")


def test_config_edit_edits_spack_yaml(mutable_mock_env_path):
    env = ev.create("test")
    with env:
        assert config("edit", "--print-file").strip() == env.manifest_path


def test_config_add_with_scope_adds_to_scope(mutable_config, mutable_mock_env_path):
    """Test adding to non-env config scope with an active environment"""
    env = ev.create("test")
    with env:
        config("--scope=user", "add", "config:install_tree:root:/usr")
    assert spack.config.get("config:install_tree:root", scope="user") == "/usr"


def test_config_edit_fails_correctly_with_no_env(mutable_mock_env_path):
    output = config("edit", "--print-file", fail_on_error=False)
    assert "requires a section argument or an active environment" in output


def test_config_list():
    output = config("list")
    assert "compilers" in output
    assert "packages" in output


def test_config_add(mutable_empty_config):
    config("add", "config:dirty:true")
    output = config("get", "config")

    assert (
        output
        == """config:
  dirty: true
"""
    )


def test_config_add_list(mutable_empty_config):
    config("add", "config:template_dirs:test1")
    config("add", "config:template_dirs:[test2]")
    config("add", "config:template_dirs:test3")
    output = config("get", "config")

    assert (
        output
        == """config:
  template_dirs:
  - test3
  - test2
  - test1
"""
    )


def test_config_add_override(mutable_empty_config):
    config("--scope", "site", "add", "config:template_dirs:test1")
    config("add", "config:template_dirs:[test2]")
    output = config("get", "config")

    assert (
        output
        == """config:
  template_dirs:
  - test2
  - test1
"""
    )

    config("add", "config::template_dirs:[test2]")
    output = config("get", "config")

    assert (
        output
        == """config:
  template_dirs:
  - test2
"""
    )


def test_config_add_override_leaf(mutable_empty_config):
    config("--scope", "site", "add", "config:template_dirs:test1")
    config("add", "config:template_dirs:[test2]")
    output = config("get", "config")

    assert (
        output
        == """config:
  template_dirs:
  - test2
  - test1
"""
    )

    config("add", "config:template_dirs::[test2]")
    output = config("get", "config")

    assert (
        output
        == """config:
  'template_dirs:':
  - test2
"""
    )


def test_config_add_update_dict(mutable_empty_config):
    config("add", "packages:hdf5:version:[1.0.0]")
    output = config("get", "packages")

    expected = "packages:\n  hdf5:\n    version: [1.0.0]\n"
    assert output == expected


def test_config_with_c_argument(mutable_empty_config):
    # I don't know how to add a spack argument to a Spack Command, so we test this way
    config_file = "config:install_tree:root:/path/to/config.yaml"
    parser = spack.main.make_argument_parser()
    args = parser.parse_args(["-c", config_file])
    assert config_file in args.config_vars

    # Add the path to the config
    config("add", args.config_vars[0], scope="command_line")
    output = config("get", "config")
    assert "config:\n  install_tree:\n    root: /path/to/config.yaml" in output


def test_config_add_ordered_dict(mutable_empty_config):
    config("add", "mirrors:first:/path/to/first")
    config("add", "mirrors:second:/path/to/second")
    output = config("get", "mirrors")

    assert (
        output
        == """mirrors:
  first: /path/to/first
  second: /path/to/second
"""
    )


def test_config_add_interpret_oneof(mutable_empty_config):
    # Regression test for a bug that would raise a validation error
    config("add", "packages:all:target:[x86_64]")
    config("add", "packages:all:variants:~shared")


def test_config_add_invalid_fails(mutable_empty_config):
    config("add", "packages:all:variants:+debug")
    with pytest.raises((spack.config.ConfigFormatError, AttributeError)):
        config("add", "packages:all:True")


def test_config_add_from_file(mutable_empty_config, tmp_path: pathlib.Path):
    contents = """spack:
  config:
    dirty: true
"""

    file = str(tmp_path / "spack.yaml")
    with open(file, "w", encoding="utf-8") as f:
        f.write(contents)
    config("add", "-f", file)
    output = config("get", "config")

    assert (
        output
        == """config:
  dirty: true
"""
    )


def test_config_add_from_file_multiple(mutable_empty_config, tmp_path: pathlib.Path):
    contents = """spack:
  config:
    dirty: true
    template_dirs: [test1]
"""

    file = str(tmp_path / "spack.yaml")
    with open(file, "w", encoding="utf-8") as f:
        f.write(contents)
    config("add", "-f", file)
    output = config("get", "config")

    assert (
        output
        == """config:
  dirty: true
  template_dirs: [test1]
"""
    )


def test_config_add_override_from_file(mutable_empty_config, tmp_path: pathlib.Path):
    config("--scope", "site", "add", "config:template_dirs:test1")
    contents = """spack:
  config::
    template_dirs: [test2]
"""

    file = str(tmp_path / "spack.yaml")
    with open(file, "w", encoding="utf-8") as f:
        f.write(contents)
    config("add", "-f", file)
    output = config("get", "config")

    assert (
        output
        == """config:
  template_dirs: [test2]
"""
    )


def test_config_add_override_leaf_from_file(mutable_empty_config, tmp_path: pathlib.Path):
    config("--scope", "site", "add", "config:template_dirs:test1")
    contents = """spack:
  config:
    template_dirs:: [test2]
"""

    file = str(tmp_path / "spack.yaml")
    with open(file, "w", encoding="utf-8") as f:
        f.write(contents)
    config("add", "-f", file)
    output = config("get", "config")

    assert (
        output
        == """config:
  'template_dirs:': [test2]
"""
    )


def test_config_add_update_dict_from_file(mutable_empty_config, tmp_path: pathlib.Path):
    config("add", "packages:all:require:['%gcc']")

    # contents to add to file
    contents = """spack:
  packages:
    all:
      target: [x86_64]
"""

    # create temp file and add it to config
    file = str(tmp_path / "spack.yaml")
    with open(file, "w", encoding="utf-8") as f:
        f.write(contents)
    config("add", "-f", file)

    # get results
    output = config("get", "packages")

    # added config comes before prior config
    expected = """packages:
  all:
    target: [x86_64]
    require: ['%gcc']
"""

    assert expected == output


def test_config_add_invalid_file_fails(tmp_path: pathlib.Path):
    # contents to add to file
    # invalid because version requires a list
    contents = """spack:
  packages:
    hdf5:
      version: 1.0.0
"""

    # create temp file and add it to config
    file = str(tmp_path / "spack.yaml")
    with open(file, "w", encoding="utf-8") as f:
        f.write(contents)

    with pytest.raises((spack.config.ConfigFormatError)):
        config("add", "-f", file)


def test_config_remove_value(mutable_empty_config):
    config("add", "config:dirty:true")
    config("remove", "config:dirty:true")
    output = config("get", "config")

    assert (
        output
        == """config: {}
"""
    )


def test_config_remove_alias_rm(mutable_empty_config):
    config("add", "config:dirty:true")
    config("rm", "config:dirty:true")
    output = config("get", "config")

    assert (
        output
        == """config: {}
"""
    )


def test_config_remove_dict(mutable_empty_config):
    config("add", "config:dirty:true")
    config("rm", "config:dirty")
    output = config("get", "config")

    assert (
        output
        == """config: {}
"""
    )


def test_remove_from_list(mutable_empty_config):
    config("add", "config:template_dirs:test1")
    config("add", "config:template_dirs:[test2]")
    config("add", "config:template_dirs:test3")
    config("remove", "config:template_dirs:test2")
    output = config("get", "config")

    assert (
        output
        == """config:
  template_dirs:
  - test3
  - test1
"""
    )


def test_remove_list(mutable_empty_config):
    config("add", "config:template_dirs:test1")
    config("add", "config:template_dirs:[test2]")
    config("add", "config:template_dirs:test3")
    config("remove", "config:template_dirs:[test2]")
    output = config("get", "config")

    assert (
        output
        == """config:
  template_dirs:
  - test3
  - test1
"""
    )


def test_config_add_to_env(mutable_empty_config, mutable_mock_env_path):
    env("create", "test")
    with ev.read("test"):
        config("add", "config:dirty:true")
        output = config("get")

    expected = """  config:
    dirty: true
"""
    assert expected in output


def test_config_add_to_env_preserve_comments(
    mutable_empty_config, mutable_mock_env_path, tmp_path: pathlib.Path
):
    filepath = str(tmp_path / "spack.yaml")
    manifest = """# comment
spack:  # comment
  # comment
  specs:  # comment
  - foo  # comment
  # comment
  view: true  # comment
  packages:  # comment
    # comment
    all: # comment
      # comment
      compiler: [gcc] # comment
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(manifest)
    env = ev.Environment(str(tmp_path))
    with env:
        config("add", "config:dirty:true")
        output = config("get")

    assert "# comment" in output
    assert "dirty: true" in output


def test_config_remove_from_env(mutable_empty_config, mutable_mock_env_path):
    env("create", "test")
    with ev.read("test"):
        config("add", "config:dirty:true")
        output = config("get")
    assert "dirty: true" in output

    with ev.read("test"):
        config("rm", "config:dirty")
        output = config("get")
    assert "dirty: true" not in output


def test_config_update_not_needed(mutable_config):
    data_before = spack.config.get("repos")
    config("update", "-y", "repos")
    data_after = spack.config.get("repos")
    assert data_before == data_after


def test_config_update_shared_linking(mutable_config):
    # Old syntax: config:shared_linking:rpath/runpath
    # New syntax: config:shared_linking:{type:rpath/runpath,bind:True/False}
    with spack.config.override("config:shared_linking", "runpath"):
        assert spack.config.get("config:shared_linking:type") == "runpath"
        assert not spack.config.get("config:shared_linking:bind")


def test_config_prefer_upstream(
    tmp_path_factory: pytest.TempPathFactory,
    install_mockery,
    mock_fetch,
    mutable_config,
    gen_mock_layout,
    monkeypatch,
):
    """Check that when a dependency package is recorded as installed in
    an upstream database that it is not reinstalled.
    """

    mock_db_root = str(tmp_path_factory.mktemp("mock_db_root"))
    prepared_db = spack.database.Database(mock_db_root, layout=gen_mock_layout("a"))

    for spec in ["hdf5 +mpi", "hdf5 ~mpi", "boost+debug~icu+graph", "dependency-install", "patch"]:
        dep = spack.concretize.concretize_one(spec)
        prepared_db.add(dep)

    downstream_db_root = str(tmp_path_factory.mktemp("mock_downstream_db_root"))
    db_for_test = spack.database.Database(downstream_db_root, upstream_dbs=[prepared_db])
    monkeypatch.setattr(spack.store.STORE, "db", db_for_test)

    output = config("prefer-upstream")
    scope = spack.config.default_modify_scope("packages")
    cfg_file = spack.config.CONFIG.get_config_filename(scope, "packages")
    packages = syaml.load(open(cfg_file, encoding="utf-8"))["packages"]

    # Make sure only the non-default variants are set.
    assert packages["boost"] == {"variants": "+debug +graph", "version": ["1.63.0"]}
    assert packages["dependency-install"] == {"version": ["2.0"]}
    # Ensure that neither variant gets listed for hdf5, since they conflict
    assert packages["hdf5"] == {"version": ["2.3"]}

    # Make sure a message about the conflicting hdf5's was given.
    assert "- hdf5" in output


def test_environment_config_update(tmp_path: pathlib.Path, mutable_config, monkeypatch):
    with open(tmp_path / "spack.yaml", "w", encoding="utf-8") as f:
        f.write(
            """\
spack:
  config:
    ccache: true
"""
        )

    def update_config(data):
        data["config"]["ccache"] = False
        return True

    monkeypatch.setattr(spack.schema.config, "update", update_config)

    with ev.Environment(str(tmp_path)):
        config("update", "-y", "config")

    with ev.Environment(str(tmp_path)) as e:
        assert not e.manifest.yaml_content["spack"]["config"]["ccache"]
