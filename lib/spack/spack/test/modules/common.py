# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import stat
import types

import pytest

import spack.cmd.modules
import spack.concretize
import spack.error
import spack.modules
import spack.modules.common
import spack.modules.tcl
import spack.package_base
import spack.package_prefs
import spack.repo
import spack.store
from spack.config import Configuration
from spack.modules.common import UpstreamModuleIndex
from spack.old_installer import PackageInstaller
from spack.util.filesystem import readlink

pytestmark = [
    pytest.mark.not_on_windows("does not run on windows"),
    pytest.mark.usefixtures("mock_modules_root"),
]


def test_update_dictionary_extending_list():
    target = {"foo": {"a": 1, "b": 2, "d": 4}, "bar": [1, 2, 4], "baz": "foobar"}
    update = {"foo": {"c": 3}, "bar": [3], "baz": "foobaz", "newkey": {"d": 4}}
    spack.modules.common.update_dictionary_extending_lists(target, update)
    assert len(target) == 4
    assert len(target["foo"]) == 4
    assert len(target["bar"]) == 4
    assert target["baz"] == "foobaz"


@pytest.fixture()
def mock_module_defaults(monkeypatch):
    def impl(*args):
        # No need to patch both types because neither override base
        monkeypatch.setattr(
            spack.modules.common.BaseConfiguration, "defaults", [arg for arg in args]
        )

    return impl


@pytest.fixture()
def mock_module_defaults_format(monkeypatch):
    def impl(value):
        monkeypatch.setattr(spack.modules.common.BaseConfiguration, "defaults_format", value)

    return impl


@pytest.fixture()
def mock_module_per_spec_filename(monkeypatch, tmp_path):
    """Modules of all specs are written with distinct file names in the same directory."""
    monkeypatch.setattr(
        spack.modules.common.FileLayout,
        "filename",
        property(lambda self: str(tmp_path / self.spec.format("{name}-{version}"))),
    )
    yield str(tmp_path)


@pytest.fixture()
def mock_package_perms(monkeypatch):
    perms = stat.S_IRGRP | stat.S_IWGRP
    monkeypatch.setattr(spack.package_prefs, "get_package_permissions", lambda spec: perms)

    yield perms


def test_modules_written_with_proper_permissions(
    mock_module_filename, mock_package_perms, mock_packages, config
):
    spec = spack.concretize.concretize_one("mpileaks")

    # The code tested is common to all module types, but has to be tested from
    # one. Tcl picked at random
    generator = spack.modules.tcl.TclModulefileWriter.from_spec(spec, "default")
    generator.write()

    assert mock_package_perms & os.stat(mock_module_filename).st_mode == mock_package_perms


@pytest.mark.parametrize("module_type", ["tcl", "lmod"])
def test_modules_default_symlink(
    module_type, mock_packages, mock_module_filename, mock_module_defaults, config
):
    spec = spack.concretize.concretize_one("mpileaks@2.3")
    mock_module_defaults(spec.format("{name}{@version}"), True)

    generator_cls = spack.modules.module_types[module_type]
    generator = generator_cls.from_spec(spec, "default")
    generator.write()

    link_path = os.path.join(os.path.dirname(mock_module_filename), "default")
    assert os.path.islink(link_path)
    assert readlink(link_path) == mock_module_filename

    generator.remove()
    assert not os.path.lexists(link_path)


@pytest.mark.parametrize("module_type", ["tcl", "lmod"])
def test_modules_default_symlink_removed_when_not_default_anymore(
    module_type, mock_packages, mock_module_filename, mock_module_defaults, config
):
    """Tests the removal of the default symlink when module stops matching defaults."""
    spec = spack.concretize.concretize_one("mpileaks@2.3")
    mock_module_defaults(spec.format("{name}{@version}"))

    generator_cls = spack.modules.module_types[module_type]
    generator = generator_cls.from_spec(spec, "default")
    generator.write()

    link_path = os.path.join(os.path.dirname(mock_module_filename), "default")
    assert readlink(link_path) == mock_module_filename

    # module is not the default anymore, symlink is removed when module is rewritten
    mock_module_defaults()
    generator.write(overwrite=True)
    assert not os.path.lexists(link_path)


@pytest.mark.parametrize("module_type", ["tcl", "lmod"])
def test_modules_default_symlink_of_other_module_preserved(
    module_type, mock_packages, mock_module_filename, mock_module_defaults, config
):
    """Tests that a default symlink not targeting this module file is left untouched."""
    spec = spack.concretize.concretize_one("mpileaks@2.3")
    mock_module_defaults()

    generator_cls = spack.modules.module_types[module_type]
    generator = generator_cls.from_spec(spec, "default")

    # default symlink targets another module file
    other_module = os.path.join(os.path.dirname(mock_module_filename), "other-module")
    link_path = os.path.join(os.path.dirname(mock_module_filename), "default")
    os.symlink(other_module, link_path)

    generator.write()
    assert readlink(link_path) == other_module

    generator.remove()
    assert readlink(link_path) == other_module


@pytest.mark.parametrize("module_type", ["tcl", "lmod"])
def test_modules_default_symlink_removal_failure_ignored(
    module_type, monkeypatch, mock_packages, mock_module_filename, mock_module_defaults, config
):
    """Tests that a failure to remove the default symlink does not abort module update."""
    spec = spack.concretize.concretize_one("mpileaks@2.3")
    mock_module_defaults(spec.format("{name}{@version}"))

    generator_cls = spack.modules.module_types[module_type]
    generator = generator_cls.from_spec(spec, "default")
    generator.write()

    link_path = os.path.join(os.path.dirname(mock_module_filename), "default")
    assert readlink(link_path) == mock_module_filename

    real_unlink = os.unlink

    def raising_unlink(path, *args, **kwargs):
        if str(path) == link_path:
            raise OSError(f"cannot unlink {path}")
        return real_unlink(path, *args, **kwargs)

    monkeypatch.setattr(os, "unlink", raising_unlink)
    generator.update_module_defaults(remove=True)
    assert readlink(link_path) == mock_module_filename


@pytest.mark.parametrize("module_type", ["tcl", "lmod"])
def test_modules_default_modulerc(
    module_type,
    mock_packages,
    mock_module_filename,
    mock_module_defaults,
    mock_module_defaults_format,
    config,
):
    """Tests the definition and removal of default version statement in modulerc."""
    spec = spack.concretize.concretize_one("mpileaks@2.3")
    mock_module_defaults(spec.format("{name}{@version}"))
    mock_module_defaults_format("modulerc")

    generator_cls = spack.modules.module_types[module_type]
    generator = generator_cls.from_spec(spec, "default")
    generator.write()

    default_version_cmd = generator.default_version_cmd_format % generator.layout.use_name
    assert os.path.exists(generator.layout.modulerc)
    with open(generator.layout.modulerc, encoding="utf-8") as f:
        content = f.read().splitlines()
    assert content.count(default_version_cmd) == 1

    # no default symlink is created with modulerc format
    link_path = os.path.join(os.path.dirname(mock_module_filename), "default")
    assert not os.path.lexists(link_path)

    # module removal also removes its default version statement
    generator.remove()
    assert not os.path.exists(generator.layout.modulerc)


@pytest.mark.parametrize("module_type", ["tcl", "lmod"])
def test_modules_default_format_transition(
    module_type,
    mock_packages,
    mock_module_filename,
    mock_module_defaults,
    mock_module_defaults_format,
    config,
):
    """Tests the conversion of the default version definition when defaults_format changes."""
    spec = spack.concretize.concretize_one("mpileaks@2.3")
    mock_module_defaults(spec.format("{name}{@version}"))

    generator_cls = spack.modules.module_types[module_type]
    generator = generator_cls.from_spec(spec, "default")
    link_path = os.path.join(os.path.dirname(mock_module_filename), "default")
    default_version_cmd = generator.default_version_cmd_format % generator.layout.use_name

    # default version is initially defined with a symlink
    generator.write()
    assert readlink(link_path) == mock_module_filename
    assert not os.path.exists(generator.layout.modulerc)

    # switching to modulerc format converts the definition when module is rewritten
    mock_module_defaults_format("modulerc")
    generator.write(overwrite=True)
    assert not os.path.lexists(link_path)
    with open(generator.layout.modulerc, encoding="utf-8") as f:
        content = f.read().splitlines()
    assert default_version_cmd in content

    # switching back to symlink format converts the definition again
    mock_module_defaults_format("symlink")
    generator.write(overwrite=True)
    assert readlink(link_path) == mock_module_filename
    assert not os.path.exists(generator.layout.modulerc)


@pytest.mark.parametrize("module_type", ["tcl", "lmod"])
def test_modules_default_target_and_format_changed_at_once(
    module_type,
    mock_packages,
    mock_module_per_spec_filename,
    mock_module_defaults,
    mock_module_defaults_format,
    config,
):
    """Tests the conversion when both the default target and defaults_format change."""
    mock_module_defaults("mpileaks@2.3")
    mock_module_defaults_format("symlink")
    generator_cls = spack.modules.module_types[module_type]

    spec = spack.concretize.concretize_one("mpileaks@2.3")
    generator = generator_cls.from_spec(spec, "default")
    spec_alt = spack.concretize.concretize_one("mpileaks@2.1")
    generator_alt = generator_cls.from_spec(spec_alt, "default")
    generator.write()
    generator_alt.write()

    link_path = os.path.join(mock_module_per_spec_filename, "default")
    default_version_cmd = generator.default_version_cmd_format % generator.layout.use_name
    default_version_cmd_alt = (
        generator_alt.default_version_cmd_format % generator_alt.layout.use_name
    )
    assert readlink(link_path) == generator.layout.filename
    assert not os.path.exists(generator.layout.modulerc)

    # default becomes the other module and format becomes modulerc at once: writing the
    # new default module alone drops the former default symlink and defines the new
    # default version in modulerc
    mock_module_defaults("mpileaks@2.1")
    mock_module_defaults_format("modulerc")
    generator_alt.write(overwrite=True)
    assert not os.path.lexists(link_path)
    with open(generator.layout.modulerc, encoding="utf-8") as f:
        content = f.read().splitlines()
    assert default_version_cmd not in content
    assert content.count(default_version_cmd_alt) == 1

    # rewriting the former default module changes nothing
    generator.write(overwrite=True)
    assert not os.path.lexists(link_path)
    with open(generator.layout.modulerc, encoding="utf-8") as f:
        content = f.read().splitlines()
    assert default_version_cmd not in content
    assert content.count(default_version_cmd_alt) == 1

    # default and format are changed back at once: writing the new default module alone
    # drops the default version statement of the former default and creates the symlink
    mock_module_defaults("mpileaks@2.3")
    mock_module_defaults_format("symlink")
    generator.write(overwrite=True)
    assert readlink(link_path) == generator.layout.filename
    assert not os.path.exists(generator.layout.modulerc)

    # rewriting the former default module changes nothing
    generator_alt.write(overwrite=True)
    assert readlink(link_path) == generator.layout.filename
    assert not os.path.exists(generator.layout.modulerc)


@pytest.mark.parametrize("module_type", ["tcl", "lmod"])
@pytest.mark.parametrize("defaults_format", ["symlink", "modulerc"])
def test_modules_default_last_generated_wins(
    module_type,
    defaults_format,
    mock_packages,
    mock_module_per_spec_filename,
    mock_module_defaults,
    mock_module_defaults_format,
    config,
):
    """Tests that when multiple modules match defaults, the last one generated wins."""
    mock_module_defaults("mpileaks")
    mock_module_defaults_format(defaults_format)
    generator_cls = spack.modules.module_types[module_type]

    spec = spack.concretize.concretize_one("mpileaks@2.3")
    generator = generator_cls.from_spec(spec, "default")
    generator.write()

    spec_alt = spack.concretize.concretize_one("mpileaks@2.1")
    generator_alt = generator_cls.from_spec(spec_alt, "default")
    generator_alt.write()

    if defaults_format == "symlink":
        link_path = os.path.join(mock_module_per_spec_filename, "default")
        assert readlink(link_path) == generator_alt.layout.filename
    else:
        default_version_cmd = generator.default_version_cmd_format % generator.layout.use_name
        default_version_cmd_alt = (
            generator_alt.default_version_cmd_format % generator_alt.layout.use_name
        )
        with open(generator_alt.layout.modulerc, encoding="utf-8") as f:
            content = f.read().splitlines()
        assert default_version_cmd not in content
        assert content.count(default_version_cmd_alt) == 1


@pytest.mark.parametrize("module_type", ["tcl", "lmod"])
def test_modules_default_modulerc_new_default_replaces_former(
    module_type,
    mock_packages,
    mock_module_filename,
    mock_module_defaults,
    mock_module_defaults_format,
    config,
):
    """Tests that a new default module drops the default version statement of the former one."""
    mock_module_defaults_format("modulerc")
    generator_cls = spack.modules.module_types[module_type]

    spec = spack.concretize.concretize_one("mpileaks@2.3")
    mock_module_defaults(spec.format("{name}{@version}"))
    generator = generator_cls.from_spec(spec, "default")
    generator.write()

    spec_alt = spack.concretize.concretize_one("mpileaks@2.1")
    mock_module_defaults(spec_alt.format("{name}{@version}"))
    generator_alt = generator_cls.from_spec(spec_alt, "default")
    generator_alt.write(overwrite=True)

    default_version_cmd = generator.default_version_cmd_format % generator.layout.use_name
    default_version_cmd_alt = (
        generator_alt.default_version_cmd_format % generator_alt.layout.use_name
    )
    with open(generator_alt.layout.modulerc, encoding="utf-8") as f:
        content = f.read().splitlines()
    assert default_version_cmd not in content
    assert content.count(default_version_cmd_alt) == 1


@pytest.mark.parametrize("module_type", ["tcl", "lmod"])
def test_modules_default_modulerc_coexists_with_hiddenness(
    module_type,
    monkeypatch,
    mock_packages,
    mock_module_filename,
    mock_module_defaults,
    mock_module_defaults_format,
    config,
):
    """Tests that default version and hiddenness statements update independently in modulerc."""
    spec = spack.concretize.concretize_one("mpileaks@2.3")
    mock_module_defaults(spec.format("{name}{@version}"))
    mock_module_defaults_format("modulerc")
    monkeypatch.setattr(spack.modules.common.BaseConfiguration, "hidden", True)

    generator_cls = spack.modules.module_types[module_type]
    generator = generator_cls.from_spec(spec, "default")
    generator.write()

    hide_cmd = generator.hide_cmd_format % generator.layout.use_name
    default_version_cmd = generator.default_version_cmd_format % generator.layout.use_name
    with open(generator.layout.modulerc, encoding="utf-8") as f:
        content = f.read().splitlines()
    assert content.count(hide_cmd) == 1
    assert content.count(default_version_cmd) == 1

    # module is not the default anymore: its default version statement is dropped while
    # its hiddenness statement is preserved
    mock_module_defaults()
    generator.write(overwrite=True)
    with open(generator.layout.modulerc, encoding="utf-8") as f:
        content = f.read().splitlines()
    assert content.count(hide_cmd) == 1
    assert default_version_cmd not in content

    # module removal drops the whole modulerc file
    generator.remove()
    assert not os.path.exists(generator.layout.modulerc)


class MockDb:
    def __init__(self, db_ids, spec_hash_to_db):
        self.upstream_dbs = db_ids
        self.spec_hash_to_db = spec_hash_to_db

    def db_for_spec_hash(self, spec_hash):
        return self.spec_hash_to_db.get(spec_hash)

    def installed_upstream(self, spec):
        return self.spec_hash_to_db.get(spec.dag_hash()) is not None


class MockSpec:
    def __init__(self, unique_id):
        self.unique_id = unique_id

    def dag_hash(self):
        return self.unique_id


def test_upstream_module_index():
    s1 = MockSpec("spec-1")
    s2 = MockSpec("spec-2")
    s3 = MockSpec("spec-3")
    s4 = MockSpec("spec-4")

    tcl_module_index = """\
module_index:
  {0}:
    path: /path/to/a
    use_name: a
""".format(s1.dag_hash())

    module_indices = [{"tcl": spack.modules.common._read_module_index(tcl_module_index)}, {}]

    dbs = ["d0", "d1"]

    mock_db = MockDb(dbs, {s1.dag_hash(): "d0", s2.dag_hash(): "d1", s3.dag_hash(): "d0"})
    upstream_index = UpstreamModuleIndex(mock_db, module_indices)

    m1 = upstream_index.upstream_module(s1, "tcl")
    assert m1.path == "/path/to/a"

    # No modules are defined for the DB associated with s2
    assert not upstream_index.upstream_module(s2, "tcl")

    # Modules are defined for the index associated with s1, but none are
    # defined for the requested type
    assert not upstream_index.upstream_module(s1, "lmod")

    # A module is registered with a DB and the associated module index has
    # modules of the specified type defined, but not for the requested spec
    assert not upstream_index.upstream_module(s3, "tcl")

    # The spec isn't recorded as installed in any of the DBs
    with pytest.raises(spack.error.SpackError):
        upstream_index.upstream_module(s4, "tcl")


def test_get_module_upstream(monkeypatch):
    s1 = MockSpec("spec-1")

    tcl_module_index = """\
module_index:
  {0}:
    path: /path/to/a
    use_name: a
""".format(s1.dag_hash())

    module_indices = [{}, {"tcl": spack.modules.common._read_module_index(tcl_module_index)}]

    dbs = ["d0", "d1"]

    mock_db = MockDb(dbs, {s1.dag_hash(): "d1"})
    upstream_index = UpstreamModuleIndex(mock_db, module_indices)

    monkeypatch.setattr(spack.store, "STORE", types.SimpleNamespace(db=mock_db))
    try:
        old_index = spack.modules.common.upstream_module_index
        spack.modules.common.upstream_module_index = upstream_index

        m1_path = spack.modules.get_module("tcl", s1, True)
        assert m1_path == "/path/to/a"
    finally:
        spack.modules.common.upstream_module_index = old_index


@pytest.mark.regression("14347")
def test_load_installed_package_not_in_repo(install_mockery, mock_fetch, monkeypatch):
    """Test that installed packages that have been removed are still loadable"""
    spec = spack.concretize.concretize_one("trivial-install-test-package")
    PackageInstaller([spec.package], explicit=True).install()
    spack.modules.module_types["tcl"].from_spec(spec, "default", True).write()

    def find_nothing(*args):
        raise spack.repo.UnknownPackageError("Repo package access is disabled for test")

    # Mock deletion of the package
    spec._package = None
    monkeypatch.setattr(spack.repo.PATH, "get", find_nothing)
    with pytest.raises(spack.repo.UnknownPackageError):
        spec.package

    module_path = spack.modules.get_module("tcl", spec, True)
    assert module_path

    spack.package_base.PackageBase.uninstall_by_spec(spec)


@pytest.mark.regression("37649")
def test_check_module_set_name(mutable_config: Configuration):
    """Tests that modules set name are validated correctly and an error is reported if the
    name we require does not exist or is reserved by the configuration."""
    # Minimal modules.yaml config.
    mutable_config.set(
        "modules",
        {
            "prefix_inspections": {"./bin": ["PATH"]},
            # module sets
            "first": {},
            "second": {},
        },
    )

    # Valid module set name
    spack.cmd.modules.check_module_set_name("first")

    # Invalid module set names
    msg = "Valid module set names are"
    with pytest.raises(spack.error.ConfigError, match=msg):
        spack.cmd.modules.check_module_set_name("prefix_inspections")

    with pytest.raises(spack.error.ConfigError, match=msg):
        spack.cmd.modules.check_module_set_name("third")
