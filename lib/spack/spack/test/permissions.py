# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib
import stat

import pytest

import spack.util.filesystem as fs
from spack.util.file_permissions import InvalidPermissionsError, set_permissions

pytestmark = pytest.mark.not_on_windows("chmod unsupported on Windows")


def ensure_known_group(path):
    """Ensure that the group of a file is one that's actually in our group list.

    On systems with remote groups, the primary user group may be remote and may not
    exist on the local system (i.e., it might just be a number). Trying to use chmod to
    setgid can fail silently in situations like this.
    """
    uid = os.getuid()
    gid = fs.group_ids(uid)[0]
    os.chown(path, uid, gid)


def test_chmod_real_entries_ignores_suid_sgid(tmp_path: pathlib.Path):
    path = tmp_path / "file"
    path.touch()
    mode = stat.S_ISUID | stat.S_ISGID | stat.S_ISVTX
    os.chmod(str(path), mode)
    mode = os.stat(str(path)).st_mode  # adds a high bit we aren't concerned with

    perms = stat.S_IRWXU
    set_permissions(str(path), perms, perms)

    assert os.stat(str(path)).st_mode == mode | perms & ~stat.S_IXUSR


def test_chmod_rejects_group_writable_suid(tmp_path: pathlib.Path):
    path = tmp_path / "file"
    path.touch()
    mode = stat.S_ISUID
    os.chmod(str(path), mode)

    perms = stat.S_IWGRP
    with pytest.raises(InvalidPermissionsError):
        set_permissions(str(path), perms, perms)


def test_chmod_rejects_world_writable_suid(tmp_path: pathlib.Path):
    path = tmp_path / "file"
    path.touch()
    mode = stat.S_ISUID
    os.chmod(str(path), mode)

    perms = stat.S_IWOTH
    with pytest.raises(InvalidPermissionsError):
        set_permissions(str(path), perms, perms)


def test_chmod_rejects_world_writable_sgid(tmp_path: pathlib.Path):
    path = tmp_path / "file"
    path.touch()
    ensure_known_group(str(path))

    mode = stat.S_ISGID
    os.chmod(str(path), mode)

    perms = stat.S_IWOTH
    with pytest.raises(InvalidPermissionsError):
        set_permissions(str(path), perms, perms)


def _make_tree(tmp_path: pathlib.Path) -> pathlib.Path:
    outside = tmp_path / "outside"
    outside.mkdir(mode=0o700)
    (outside / "file").touch(mode=0o600)
    (outside / "subdir").mkdir(mode=0o700)
    (outside / "subdir" / "file").touch(mode=0o600)

    prefix = tmp_path / "prefix"
    (prefix / "bin").mkdir(mode=0o700, parents=True)
    (prefix / "bin" / "exe").touch(mode=0o700)
    (prefix / "bin" / "data").touch(mode=0o600)
    (prefix / "file_link").symlink_to(outside / "file")
    (prefix / "dir_link").symlink_to(outside / "subdir")
    (prefix / "dangling_link").symlink_to(tmp_path / "does-not-exist")
    return prefix


def _mode(path: pathlib.Path) -> int:
    return stat.S_IMODE(os.lstat(path).st_mode)


def test_set_permissions_recursive(tmp_path: pathlib.Path):
    prefix = _make_tree(tmp_path)
    set_permissions(str(prefix), 0o755, 0o755, os.lstat(prefix).st_gid)

    assert _mode(prefix) == 0o755
    assert _mode(prefix / "bin") == 0o755
    assert _mode(prefix / "bin" / "exe") == 0o755
    assert _mode(prefix / "bin" / "data") == 0o644

    # symlink targets outside the prefix are untouched
    assert _mode(tmp_path / "outside" / "file") == 0o600
    assert _mode(tmp_path / "outside" / "subdir") == 0o700
    assert _mode(tmp_path / "outside" / "subdir" / "file") == 0o600


def test_set_permissions_no_changes(tmp_path: pathlib.Path, monkeypatch):
    prefix = _make_tree(tmp_path)
    gid = os.lstat(prefix).st_gid
    set_permissions(str(prefix), 0o755, 0o755, gid)

    def _fail(*args, **kwargs):
        raise AssertionError("permissions already set")

    monkeypatch.setattr(os, "chmod", _fail)
    monkeypatch.setattr(os, "chown", _fail)
    monkeypatch.setattr(os, "lchown", _fail)
    set_permissions(str(prefix), 0o755, 0o755, gid)


@pytest.mark.skipif(len(fs.group_ids()) < 2, reason="requires a secondary group")
def test_set_permissions_group(tmp_path: pathlib.Path):
    prefix = _make_tree(tmp_path)
    ensure_known_group(str(prefix / "bin" / "exe"))
    os.chmod(prefix / "bin" / "exe", 0o700 | stat.S_ISGID)
    gid = next(g for g in fs.group_ids() if g != os.lstat(prefix / "bin" / "exe").st_gid)

    set_permissions(str(prefix), 0o755, 0o755, gid)

    for path in (prefix, prefix / "bin", prefix / "bin" / "exe", prefix / "dangling_link"):
        assert os.lstat(path).st_gid == gid

    # sgid survives the group change
    assert _mode(prefix / "bin" / "exe") == 0o755 | stat.S_ISGID
