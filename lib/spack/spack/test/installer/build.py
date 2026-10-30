# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for the installer.build module (PrefixPivoter and prefix management)."""

import json
import pathlib
from types import SimpleNamespace

import pytest

import spack.hooks
import spack.hooks.autopush as autopush_hook
import spack.hooks.write_install_manifest as manifest_hook
import spack.installer.build as build
import spack.util.timer
from spack.installer.build import (
    OVERWRITE_GARBAGE_SUFFIX,
    BinaryCacheMiss,
    PostInstallState,
    PrefixPivoter,
)


@pytest.fixture
def existing_prefix(tmp_path: pathlib.Path) -> pathlib.Path:
    """Creates a standard existing prefix with content."""
    prefix = tmp_path / "existing_prefix"
    prefix.mkdir()
    (prefix / "old_file").write_text("old content")
    return prefix


class TestPrefixPivoter:
    """Tests for the PrefixPivoter class."""

    def test_no_existing_prefix(self, tmp_path: pathlib.Path):
        """Test installation when prefix doesn't exist yet."""
        prefix = tmp_path / "new_prefix"

        with PrefixPivoter(str(prefix)):
            prefix.mkdir()
            (prefix / "installed_file").write_text("content")

        assert prefix.exists()
        assert (prefix / "installed_file").read_text() == "content"

    def test_existing_prefix_success_cleans_up_old_prefix(
        self, tmp_path: pathlib.Path, existing_prefix: pathlib.Path
    ):
        """Test that an existing prefix is moved aside, and cleaned up on success."""
        with PrefixPivoter(str(existing_prefix)):
            assert not existing_prefix.exists()
            existing_prefix.mkdir()
            (existing_prefix / "new_file").write_text("new content")

        assert existing_prefix.exists()
        assert (existing_prefix / "new_file").exists()
        assert not (existing_prefix / "old_file").exists()
        # Only the existing_prefix directory should remain
        assert len(list(tmp_path.iterdir())) == 1

    def test_existing_prefix_failure_restores_original_prefix(
        self, tmp_path: pathlib.Path, existing_prefix: pathlib.Path
    ):
        """Test that the original prefix is restored when installation fails."""
        with pytest.raises(RuntimeError, match="simulated failure"):
            with PrefixPivoter(str(existing_prefix), keep_prefix=False):
                existing_prefix.mkdir()
                (existing_prefix / "partial_file").write_text("partial")
                raise RuntimeError("simulated failure")

        assert existing_prefix.exists()
        assert (existing_prefix / "old_file").read_text() == "old content"
        assert not (existing_prefix / "partial_file").exists()
        # Only the original prefix should remain
        assert len(list(tmp_path.iterdir())) == 1

    def test_existing_prefix_failure_no_partial_prefix_created(
        self, existing_prefix: pathlib.Path
    ):
        """Test restoration when failure occurs before the build creates the prefix dir."""
        with pytest.raises(RuntimeError, match="early failure"):
            with PrefixPivoter(str(existing_prefix)):
                raise RuntimeError("early failure")

        assert existing_prefix.exists()
        assert (existing_prefix / "old_file").read_text() == "old content"

    def test_no_existing_prefix_success(self, tmp_path: pathlib.Path):
        """Test that a fresh install with no pre-existing prefix works fine."""
        prefix = tmp_path / "new_prefix"
        with PrefixPivoter(str(prefix)):
            prefix.mkdir()
            (prefix / "installed_file").write_text("content")

        assert prefix.exists()
        # Only the new_prefix directory should remain
        assert len(list(tmp_path.iterdir())) == 1

    def test_keep_prefix_true_with_existing_prefix_keeps_failed_install(
        self, tmp_path: pathlib.Path, existing_prefix: pathlib.Path
    ):
        """Test that keep_prefix=True keeps the failed install and discards the backup."""
        with pytest.raises(RuntimeError, match="simulated failure"):
            with PrefixPivoter(str(existing_prefix), keep_prefix=True):
                existing_prefix.mkdir()
                (existing_prefix / "partial_file").write_text("partial content")
                raise RuntimeError("simulated failure")

        # The failed prefix should be kept (not the original)
        assert existing_prefix.exists()
        assert (existing_prefix / "partial_file").exists()
        assert not (existing_prefix / "old_file").exists()
        # Backup should have been removed
        assert len(list(tmp_path.iterdir())) == 1

    def test_keep_prefix_false_removes_failed_install(self, tmp_path: pathlib.Path):
        """Test that keep_prefix=False removes the failed installation (no pre-existing prefix)."""
        prefix = tmp_path / "new_prefix"

        with pytest.raises(RuntimeError, match="simulated failure"):
            with PrefixPivoter(str(prefix), keep_prefix=False):
                prefix.mkdir()
                (prefix / "partial_file").write_text("partial content")
                raise RuntimeError("simulated failure")

        # Failed prefix should be removed
        assert not prefix.exists()
        # Nothing should remain
        assert len(list(tmp_path.iterdir())) == 0

    def test_keep_prefix_true_no_existing_prefix(self, tmp_path: pathlib.Path):
        """Test failure with keep_prefix=True when no prefix existed beforehand."""
        prefix = tmp_path / "new_prefix"

        with pytest.raises(RuntimeError, match="simulated failure"):
            with PrefixPivoter(str(prefix), keep_prefix=True):
                prefix.mkdir()
                (prefix / "partial_file").write_text("partial content")
                raise RuntimeError("simulated failure")

        # The failed prefix should be kept
        assert prefix.exists()
        assert (prefix / "partial_file").exists()
        # No backup should exist
        assert len(list(tmp_path.iterdir())) == 1

    def test_failure_no_prefix_created(self, tmp_path: pathlib.Path):
        """Test failure when the prefix directory was never created."""
        prefix = tmp_path / "new_prefix"

        with pytest.raises(RuntimeError, match="simulated failure"):
            with PrefixPivoter(str(prefix), keep_prefix=False):
                # Do NOT create the prefix directory
                raise RuntimeError("simulated failure")

        # Prefix should not exist
        assert not prefix.exists()
        # Nothing should remain
        assert len(list(tmp_path.iterdir())) == 0

    def test_binary_cache_miss_with_keep_prefix_and_existing_prefix_restores_original(
        self, tmp_path: pathlib.Path, existing_prefix: pathlib.Path
    ):
        """BinaryCacheMiss bypasses keep_prefix: original prefix is restored."""
        with pytest.raises(BinaryCacheMiss), PrefixPivoter(str(existing_prefix), keep_prefix=True):
            existing_prefix.mkdir()
            (existing_prefix / "partial_file").write_text("partial content")
            raise BinaryCacheMiss("cache miss")

        assert (existing_prefix / "old_file").read_text() == "old content"
        assert not (existing_prefix / "partial_file").exists()
        assert len(list(tmp_path.iterdir())) == 1


class FailingPrefixPivoter(PrefixPivoter):
    """Test subclass that can simulate filesystem failures."""

    def __init__(
        self,
        prefix: str,
        keep_prefix: bool = False,
        fail_on_restore: bool = False,
        fail_on_move_garbage: bool = False,
    ):
        super().__init__(prefix, keep_prefix)
        self.fail_on_restore = fail_on_restore
        self.fail_on_move_garbage = fail_on_move_garbage
        self.restore_rename_count = 0

    def _rename(self, src: str, dst: str) -> None:
        if (
            self.fail_on_restore
            and self.tmp_prefix
            and src == self.tmp_prefix
            and dst == self.prefix
        ):
            self.restore_rename_count += 1
            raise OSError("Simulated rename failure during restore")

        if self.fail_on_move_garbage and dst.endswith(OVERWRITE_GARBAGE_SUFFIX):
            raise OSError("Simulated rename failure moving to garbage")

        super()._rename(src, dst)


class TestPrefixPivoterFailureRecovery:
    """Tests for edge cases and failure recovery in PrefixPivoter."""

    def test_restore_failure_leaves_backup(
        self, tmp_path: pathlib.Path, existing_prefix: pathlib.Path
    ):
        """Test that if restoration fails, the backup is not deleted."""
        pivoter = FailingPrefixPivoter(str(existing_prefix), fail_on_restore=True)

        with pytest.raises(OSError, match="Simulated rename failure during restore"):
            with pivoter:
                existing_prefix.mkdir()
                (existing_prefix / "partial_file").write_text("partial")
                raise RuntimeError("simulated failure")

        assert pivoter.restore_rename_count > 0
        # Backup directory should still exist (plus the failed prefix)
        assert len(list(tmp_path.iterdir())) == 2

    def test_garbage_move_failure_leaves_backup(
        self, tmp_path: pathlib.Path, existing_prefix: pathlib.Path
    ):
        """Test that if moving the failed install to garbage fails, the backup is preserved."""
        pivoter = FailingPrefixPivoter(str(existing_prefix), fail_on_move_garbage=True)

        with pytest.raises(OSError, match="Simulated rename failure moving to garbage"):
            with pivoter:
                existing_prefix.mkdir()
                (existing_prefix / "partial_file").write_text("partial")
                raise RuntimeError("simulated failure")

        assert (existing_prefix / "partial_file").exists()
        # Backup directory, failed prefix, and empty garbage directory should exist
        assert len(list(tmp_path.iterdir())) == 3


def _build_log_package(prefix: pathlib.Path, *, from_cache: bool = False):
    metadata = prefix / ".spack"
    metadata.mkdir(parents=True)
    return SimpleNamespace(
        prefix=str(prefix),
        install_log_path=str(metadata / "spack-build-out.txt.gz"),
        installed_from_binary_cache=from_cache,
        spec=object(),
    )


def test_spliced_cache_build_log_can_be_archived_after_manifest_removal(
    tmp_path: pathlib.Path, monkeypatch
):
    pkg = _build_log_package(tmp_path / "prefix", from_cache=True)
    manifest = pathlib.Path(pkg.prefix) / ".spack" / "install_manifest.json"
    manifest.write_text(json.dumps({pkg.prefix: {}}), encoding="utf-8")
    assert manifest.is_file()
    manifest.unlink()

    log = tmp_path / "worker.log"
    log.write_bytes(b"relocation output")
    monkeypatch.setattr(build.fp, "set_permissions_by_spec", lambda *args: None)

    build._archive_build_log(pkg, str(log))

    assert not manifest.exists()
    assert pathlib.Path(pkg.install_log_path).is_file()


def test_post_install_split_requires_manifest_hook(monkeypatch):
    monkeypatch.setattr(
        spack.hooks.post_install, "_hooks", [SimpleNamespace(__name__="spack.hooks.autopush")]
    )

    with pytest.raises(RuntimeError, match="write_install_manifest.*not registered"):
        spack.hooks.post_install_pre_manifest(None, explicit=True)
    with pytest.raises(RuntimeError, match="write_install_manifest.*not registered"):
        spack.hooks.post_install_manifest_and_after(None, explicit=True)


def test_pre_manifest_hook_failure_stops_post_install_timer(monkeypatch):
    def fail(*args, **kwargs):
        raise RuntimeError("pre-manifest hook failed")

    monkeypatch.setattr(spack.hooks, "post_install_pre_manifest", fail)
    monkeypatch.setattr(
        build, "_write_timer_json", lambda *args: pytest.fail("timer file written")
    )
    timer = spack.util.timer.Timer()

    with pytest.raises(RuntimeError, match="pre-manifest hook failed"):
        build._post_install(SimpleNamespace(), SimpleNamespace(), False, timer)

    timer._flatten()
    assert "post-install" in timer.phases
    assert "post-install" not in timer._timer_stack


def test_build_log_compression_failure_leaves_no_partial_file(tmp_path: pathlib.Path, monkeypatch):
    pkg = _build_log_package(tmp_path / "prefix")
    log = tmp_path / "worker.log"
    log.write_bytes(b"build output")

    def fail_after_partial_write(*args, **kwargs):
        kwargs["fileobj"].write(b"partial gzip data")
        raise OSError("simulated compression failure")

    spec = SimpleNamespace(prefix=pkg.prefix)
    manifest = pathlib.Path(pkg.prefix) / ".spack" / "install_manifest.json"
    manifest_calls = []

    def write_manifest(spec, explicit):
        manifest_calls.append("manifest")
        assert not pathlib.Path(pkg.install_log_path).exists()
        manifest.write_text("{}", encoding="utf-8")

    monkeypatch.setattr(build, "GzipFile", fail_after_partial_write)
    monkeypatch.setattr(manifest_hook, "post_install", write_manifest)
    monkeypatch.setattr(autopush_hook, "post_install", lambda *args, **kwargs: None)

    build._archive_build_log(pkg, str(log))
    spack.hooks.post_install_manifest_and_after(spec, explicit=True)

    assert not pathlib.Path(pkg.install_log_path).exists()
    assert list((pathlib.Path(pkg.prefix) / ".spack").iterdir()) == [manifest]
    assert manifest_calls == ["manifest"]
    assert manifest.is_file()


@pytest.mark.parametrize("failure_hook", ["manifest", "autopush"])
@pytest.mark.parametrize("keep_prefix", [False, True])
def test_deferred_hook_failure_uses_prefix_pivot_rollback(
    tmp_path: pathlib.Path, monkeypatch, failure_hook: str, keep_prefix: bool
):
    prefix = tmp_path / "prefix"
    prefix.mkdir()
    (prefix / "original").write_text("original", encoding="utf-8")
    spec = SimpleNamespace(prefix=str(prefix))

    def fail(*args, **kwargs):
        raise RuntimeError(f"{failure_hook} failed")

    monkeypatch.setattr(
        manifest_hook,
        "post_install",
        fail if failure_hook == "manifest" else lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        autopush_hook,
        "post_install",
        fail if failure_hook == "autopush" else lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        build, "_write_timer_json", lambda *args: pytest.fail("timer file written")
    )

    with pytest.raises(RuntimeError, match=f"{failure_hook} failed"):
        timer = spack.util.timer.Timer()
        timer.start("post-install")
        with PrefixPivoter(str(prefix), keep_prefix=keep_prefix):
            prefix.mkdir()
            (prefix / "partial").write_text("partial", encoding="utf-8")
            build._finish_post_install(
                SimpleNamespace(), spec, explicit=True, state=PostInstallState(timer, cache=False)
            )

    timer._flatten()
    assert "post-install" in timer.phases
    assert "post-install" not in timer._timer_stack

    if keep_prefix:
        assert not (prefix / "original").exists()
        assert (prefix / "partial").exists()
    else:
        assert (prefix / "original").read_text(encoding="utf-8") == "original"
        assert not (prefix / "partial").exists()
