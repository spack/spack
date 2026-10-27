# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import pathlib
import stat
import sys
import types
import warnings

import pytest

import spack.cmd.modules
import spack.concretize
import spack.config
import spack.error
import spack.main
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

if sys.platform != "win32":
    import grp

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

    generator.remove_installation()
    assert not os.path.lexists(link_path)


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


@pytest.mark.parametrize("module_type", ["tcl", "lmod"])
def test_modules_default_symlink_removed_with_another_root_spelling(
    module_type, tmp_path, monkeypatch, mock_packages, mock_module_defaults, config
):
    """Tests that removing a module file removes its default link, when the module root was
    spelled through a symbolic link at the time the default link was made."""
    real_root = tmp_path / "real"
    real_root.mkdir()
    link_root = tmp_path / "link"
    link_root.symlink_to(real_root)
    spec = spack.concretize.concretize_one("mpileaks@2.3")
    mock_module_defaults(spec.format("{name}{@version}"), True)
    writer_cls = spack.modules.module_types[module_type]

    monkeypatch.setattr(spack.modules.common.FileLayout, "filename", str(link_root / "module"))
    writer_cls.from_spec(spec, "default").write()
    default_link = real_root / "default"
    assert default_link.is_symlink()

    monkeypatch.setattr(spack.modules.common.FileLayout, "filename", str(real_root / "module"))
    writer_cls.from_spec(spec, "default").remove_installation()
    assert not os.path.lexists(default_link)


def test_invalid_modules_config_warns_on_module_updates(tmp_path, mutable_config, mock_packages):
    """Tests that an invalid modules configuration turns writing and removing module files into
    a warning, and that no warning is emitted when there is nothing to update."""
    spec = spack.concretize.concretize_one("mpileaks")
    (tmp_path / "modules.yaml").write_text(
        "modules:\n  default:\n    enable: [tcl]\n    tcl:\n      mpileaks@@1: {}\n"
    )
    mutable_config.push_scope(spack.config.DirectoryConfigScope("invalid", str(tmp_path)))

    with pytest.warns(UserWarning, match="modules configuration is not valid"):
        spack.modules.write_module_files([spec])
    with pytest.warns(UserWarning, match="modules configuration is not valid"):
        spack.modules.remove_module_files([spec])

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        spack.modules.write_module_files([])
        spack.modules.remove_module_files([])


def _created_module_directories(writer, root):
    return [p for p in pathlib.Path(writer.layout.filename).parents if root in p.parents]


def _group_for_test() -> int:
    """Returns a supplementary group of the user with a name, or the primary group if there is
    none.
    """
    for gid in os.getgroups():
        if gid == os.getgid():
            continue
        try:
            grp.getgrgid(gid)
        except KeyError:
            continue
        return gid
    return os.getgid()


@pytest.mark.parametrize(
    "write,added", [("group", stat.S_IRWXG), ("world", stat.S_IRWXG | stat.S_IRWXO)]
)
def test_module_directories_get_group_and_write_access_for_all_packages(
    write, added, tmp_path, mutable_config, mock_packages
):
    """Tests that the directories created for module files get the group and the write access
    configured for all packages on top of what the umask gives, also when the package of the
    module file restricts them.
    """
    gid = _group_for_test()
    mutable_config.set(
        "packages:all:permissions",
        {"read": "world", "write": write, "group": grp.getgrgid(gid).gr_name},
    )
    mutable_config.set("packages:mpileaks:permissions", {"read": "user", "write": "user"})
    reference = tmp_path / "reference"
    reference.mkdir()
    spec = spack.concretize.concretize_one("mpileaks")
    writer = spack.modules.tcl.TclModulefileWriter.from_spec(spec, "default")
    writer.write()

    expected_mode = reference.stat().st_mode | added | stat.S_ISGID
    created = _created_module_directories(writer, tmp_path)
    assert created
    for p in created:
        assert p.stat().st_mode == expected_mode
        assert p.stat().st_gid == gid


def test_refresh_delete_tree_recreates_root_with_group_and_write_access(
    tmp_path, mutable_config, database_mutable_config, monkeypatch
):
    """Tests that refreshing with ``--delete-tree`` recreates the module root with the group and
    the write access configured for all packages on top of what the umask gives.
    """
    root = tmp_path / "root"
    root.mkdir()
    monkeypatch.setattr(spack.modules.common, "root_path", lambda *args: str(root))
    gid = _group_for_test()
    mutable_config.set(
        "packages:all:permissions",
        {"read": "world", "write": "group", "group": grp.getgrgid(gid).gr_name},
    )
    reference = tmp_path / "reference"
    reference.mkdir()

    spack.main.SpackCommand("module")("tcl", "refresh", "--delete-tree", "-y")

    assert root.stat().st_mode == reference.stat().st_mode | stat.S_IRWXG | stat.S_ISGID
    assert root.stat().st_gid == gid
