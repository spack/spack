# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for the new_installer.py module"""

import pathlib
import sys
import time

import pytest

if sys.platform == "win32":
    pytest.skip("No Windows support", allow_module_level=True)

import spack.spec
from spack.new_installer import (
    OVERWRITE_GARBAGE_SUFFIX,
    JobServer,
    PackageInstaller,
    PrefixPivoter,
    _node_to_roots,
    schedule_builds,
)
from spack.test.traverse import create_dag


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


class TestPackageInstallerConstructor:
    """Tests for PackageInstaller constructor, especially capacity initialization."""

    def test_capacity_explicit_concurrent_packages(self, temporary_store, mock_packages):
        """Test that capacity is set correctly when concurrent_packages is explicitly provided."""
        spec = spack.spec.Spec("trivial-install-test-package")
        spec._mark_concrete()
        assert PackageInstaller([spec.package], concurrent_packages=5).capacity == 5
        assert PackageInstaller([spec.package], concurrent_packages=1).capacity == 1

    def test_capacity_from_config_default_one(
        self, temporary_store, mock_packages, mutable_config
    ):
        """Test that config value of 0 is treated as unlimited."""
        mutable_config.set("config:concurrent_packages", 0)
        spec = spack.spec.Spec("trivial-install-test-package")
        spec._mark_concrete()
        assert PackageInstaller([spec.package]).capacity == sys.maxsize

    def test_capacity_from_config_non_zero(self, temporary_store, mock_packages, mutable_config):
        """Test that non-0 config values are used as-is."""
        mutable_config.set("config:concurrent_packages", 1)
        spec = spack.spec.Spec("trivial-install-test-package")
        spec._mark_concrete()
        assert PackageInstaller([spec.package]).capacity == 1


class _FakeBuildGraph:
    """Minimal stand-in for BuildGraph in schedule_builds unit tests.

    Provides the two interface points that schedule_builds calls:
      - .nodes  (dict: dag_hash -> Spec)
      - .enqueue_parents(dag_hash, pending_builds)
    """

    def __init__(self, specs):
        self.nodes = {spec.dag_hash(): spec for spec in specs}

    def enqueue_parents(self, dag_hash, pending_builds):
        """Remove dag_hash from nodes; no parents in these simple unit tests."""
        self.nodes.pop(dag_hash, None)


class TestScheduleBuilds:
    """Unit tests for the module-level schedule_builds() function."""

    def _make_spec(self, name):
        """Return a minimal concrete spec suitable for locking and DB queries."""
        spec = spack.spec.Spec(name)
        spec._mark_concrete()
        return spec

    def _mark_installed(self, spec, store):
        """Create the install directory structure and register the spec in the DB as installed."""
        store.layout.create_install_directory(spec)
        store.db.add(spec, explicit=True)

    def test_not_installed_no_running_starts_build(self, temporary_store, mock_packages):
        """A fresh spec with no running builds is added to to_start."""
        spec = self._make_spec("trivial-install-test-package")
        pending = [spec.dag_hash()]
        bg = _FakeBuildGraph([spec])
        jobserver = JobServer(num_jobs=2)
        try:
            result = schedule_builds(
                pending,
                bg,
                temporary_store.db,
                temporary_store.prefix_locker,
                overwrite=set(),
                overwrite_time=0.0,
                capacity=1,
                needs_jobserver_token=False,
                jobserver=jobserver,
                explicit=set(),
            )
            assert not result.blocked
            assert len(result.to_start) == 1
            assert result.to_start[0][0] == spec.dag_hash()
            assert not result.newly_installed
            assert not pending  # removed from the pending list
        finally:
            for _, lock in result.to_start:
                lock.release_write()
            jobserver.close()

    def test_already_installed_yields_newly_installed(self, temporary_store, mock_packages):
        """A spec already in the DB is returned in newly_installed, not in to_start."""
        spec = self._make_spec("trivial-install-test-package")
        self._mark_installed(spec, temporary_store)
        pending = [spec.dag_hash()]
        bg = _FakeBuildGraph([spec])
        jobserver = JobServer(num_jobs=2)
        try:
            result = schedule_builds(
                pending,
                bg,
                temporary_store.db,
                temporary_store.prefix_locker,
                overwrite=set(),
                overwrite_time=0.0,
                capacity=1,
                needs_jobserver_token=False,
                jobserver=jobserver,
                explicit=set(),
            )
            assert not result.blocked
            assert not result.to_start
            assert len(result.newly_installed) == 1
            assert result.newly_installed[0][0] == spec.dag_hash()
            assert not pending  # removed from the pending list
        finally:
            for _, _, lock in result.newly_installed:
                lock.release_read()
            jobserver.close()

    def test_no_jobserver_token_returns_empty(self, temporary_store, mock_packages):
        """When has_running_builds=True and no token is available, nothing is started."""
        spec = self._make_spec("trivial-install-test-package")
        pending = [spec.dag_hash()]
        bg = _FakeBuildGraph([spec])
        # num_jobs=1 writes 0 tokens to the FIFO. Only the implicit token exists.
        jobserver = JobServer(num_jobs=1)
        try:
            result = schedule_builds(
                pending,
                bg,
                temporary_store.db,
                temporary_store.prefix_locker,
                overwrite=set(),
                overwrite_time=0.0,
                capacity=2,
                needs_jobserver_token=True,
                jobserver=jobserver,
                explicit=set(),
            )
            assert not result.blocked
            assert not result.to_start
            assert not result.newly_installed
            assert len(pending) == 1
        finally:
            jobserver.close()

    def test_all_locked_returns_blocked(self, temporary_store, mock_packages, monkeypatch):
        """When all pending specs are locked externally, blocked_on_locks is True."""
        spec = self._make_spec("trivial-install-test-package")
        pending = [spec.dag_hash()]
        bg = _FakeBuildGraph([spec])
        jobserver = JobServer(num_jobs=2)
        # Pre-register the lock in the prefix_locker cache, then patch try_acquire to fail.
        lock = temporary_store.prefix_locker.lock(spec)
        monkeypatch.setattr(lock, "try_acquire_write", lambda: False)
        monkeypatch.setattr(lock, "try_acquire_read", lambda: False)
        try:
            result = schedule_builds(
                pending,
                bg,
                temporary_store.db,
                temporary_store.prefix_locker,
                overwrite=set(),
                overwrite_time=0.0,
                capacity=2,
                needs_jobserver_token=False,
                jobserver=jobserver,
                explicit=set(),
            )
            assert result.blocked
            assert not result.to_start
            assert not result.newly_installed
            assert len(pending) == 1
        finally:
            jobserver.close()

    def test_overwrite_installed_spec_is_started(self, temporary_store, mock_packages):
        """A spec in the overwrite set is scheduled even when already installed."""
        spec = self._make_spec("trivial-install-test-package")
        self._mark_installed(spec, temporary_store)
        pending = [spec.dag_hash()]
        bg = _FakeBuildGraph([spec])
        jobserver = JobServer(num_jobs=2)
        try:
            result = schedule_builds(
                pending,
                bg,
                temporary_store.db,
                temporary_store.prefix_locker,
                overwrite={spec.dag_hash()},
                overwrite_time=time.time() + 100,
                capacity=1,
                needs_jobserver_token=False,
                jobserver=jobserver,
                explicit=set(),
            )
            assert not result.blocked
            assert len(result.to_start) == 1
            assert result.to_start[0][0] == spec.dag_hash()
            assert not result.newly_installed
        finally:
            for _, lock in result.to_start:
                lock.release_write()
            jobserver.close()

    def test_mixed_locked_unlocked(self, temporary_store, mock_packages, monkeypatch):
        """Only the unlocked spec enters to_start when one spec is externally locked."""
        spec_a = self._make_spec("trivial-install-test-package")
        spec_b = self._make_spec("trivial-smoke-test")
        pending = [spec_a.dag_hash(), spec_b.dag_hash()]
        bg = _FakeBuildGraph([spec_a, spec_b])
        jobserver = JobServer(num_jobs=4)
        # Patch spec_a's lock to always fail, simulating an external write lock.
        lock_a = temporary_store.prefix_locker.lock(spec_a)
        monkeypatch.setattr(lock_a, "try_acquire_write", lambda: False)
        monkeypatch.setattr(lock_a, "try_acquire_read", lambda: False)
        try:
            result = schedule_builds(
                pending,
                bg,
                temporary_store.db,
                temporary_store.prefix_locker,
                overwrite=set(),
                overwrite_time=0.0,
                capacity=2,
                needs_jobserver_token=False,
                jobserver=jobserver,
                explicit=set(),
            )
            assert not result.blocked  # spec_b was schedulable
            started_hashes = {h for h, _ in result.to_start}
            assert spec_b.dag_hash() in started_hashes
            assert spec_a.dag_hash() not in started_hashes
            assert not result.newly_installed
        finally:
            for _, lock in result.to_start:
                lock.release_write()
            jobserver.close()

    def test_write_locked_read_locked_installed_yields_newly_installed(
        self, temporary_store, mock_packages, monkeypatch
    ):
        """Write lock fails but read lock succeeds and spec is installed: treated as done.

        Simulates the case where another process finished building and downgraded its write lock
        to a read lock. The spec should appear in newly_installed. blocked remains True because no
        write lock was obtained, preventing the jobserver from firing unnecessarily.
        """
        spec = self._make_spec("trivial-install-test-package")
        self._mark_installed(spec, temporary_store)
        pending = [spec.dag_hash()]
        bg = _FakeBuildGraph([spec])
        jobserver = JobServer(num_jobs=2)
        lock = temporary_store.prefix_locker.lock(spec)
        monkeypatch.setattr(lock, "try_acquire_write", lambda: False)
        try:
            result = schedule_builds(
                pending,
                bg,
                temporary_store.db,
                temporary_store.prefix_locker,
                overwrite=set(),
                overwrite_time=0.0,
                capacity=2,
                needs_jobserver_token=False,
                jobserver=jobserver,
                explicit=set(),
            )
            assert result.blocked  # no write lock was obtained; jobserver should not fire
            assert not result.to_start
            assert len(result.newly_installed) == 1
            dag_hash, installed_spec, lock = result.newly_installed[0]
            assert dag_hash == spec.dag_hash()
            assert installed_spec == spec
            assert not pending  # spec was removed from pending
        finally:
            for _, _, lock in result.newly_installed:
                lock.release_read()
            jobserver.close()

    def test_write_locked_read_locked_not_installed_still_blocked(
        self, temporary_store, mock_packages, monkeypatch
    ):
        """Write lock fails, read lock succeeds, but spec is not in DB: retry later.

        Simulates the case where a concurrent process was killed mid-build. The read lock is
        released and the spec stays in pending; blocked should remain True.
        """
        spec = self._make_spec("trivial-install-test-package")
        pending = [spec.dag_hash()]
        bg = _FakeBuildGraph([spec])
        jobserver = JobServer(num_jobs=2)
        lock = temporary_store.prefix_locker.lock(spec)
        monkeypatch.setattr(lock, "try_acquire_write", lambda: False)
        try:
            result = schedule_builds(
                pending,
                bg,
                temporary_store.db,
                temporary_store.prefix_locker,
                overwrite=set(),
                overwrite_time=0.0,
                capacity=2,
                needs_jobserver_token=False,
                jobserver=jobserver,
                explicit=set(),
            )
            assert result.blocked
            assert not result.to_start
            assert not result.newly_installed
            assert pending == [spec.dag_hash()]  # spec stays in pending for retry
        finally:
            jobserver.close()

    def test_overwrite_handled_by_concurrent_process(self, temporary_store, mock_packages):
        """When a spec in overwrite was installed AFTER overwrite_time, another process did it."""
        spec = self._make_spec("trivial-install-test-package")
        self._mark_installed(spec, temporary_store)  # installation_time = now()
        pending = [spec.dag_hash()]
        bg = _FakeBuildGraph([spec])
        jobserver = JobServer(num_jobs=2)
        try:
            result = schedule_builds(
                pending,
                bg,
                temporary_store.db,
                temporary_store.prefix_locker,
                overwrite={spec.dag_hash()},
                overwrite_time=0.0,  # earlier than now()
                capacity=1,
                needs_jobserver_token=False,
                jobserver=jobserver,
                explicit=set(),
            )
            assert not result.blocked
            assert not result.to_start
            assert len(result.newly_installed) == 1
            assert result.newly_installed[0][0] == spec.dag_hash()
        finally:
            for _, _, lock in result.newly_installed:
                lock.release_read()
            jobserver.close()

    def test_installed_implicit_explicit_set_produces_db_update(
        self, temporary_store, mock_packages
    ):
        """An installed-implicit spec in explicit set produces a DbUpdate."""
        spec = self._make_spec("trivial-install-test-package")
        temporary_store.layout.create_install_directory(spec)
        temporary_store.db.add(spec, explicit=False)
        pending = [spec.dag_hash()]
        bg = _FakeBuildGraph([spec])
        jobserver = JobServer(num_jobs=2)
        try:
            result = schedule_builds(
                pending,
                bg,
                temporary_store.db,
                temporary_store.prefix_locker,
                overwrite=set(),
                overwrite_time=0.0,
                capacity=1,
                needs_jobserver_token=False,
                jobserver=jobserver,
                explicit={spec.dag_hash()},
            )
            assert len(result.to_mark_explicit) == 1
            assert result.to_mark_explicit[0].spec is spec
            assert len(result.newly_installed) == 1
        finally:
            for _, _, lock in result.newly_installed:
                lock.release_read()
            jobserver.close()


def test_nodes_to_roots():
    """Independent roots don't reach each other's exclusive nodes."""
    # A - B and C - D are disconnected graphs, A, B and C are "roots".
    specs = create_dag(nodes=["A", "B", "C", "D"], edges=[("A", "B", "all"), ("C", "D", "all")])
    a, b, c, d = specs["A"], specs["B"], specs["C"], specs["D"]
    node_to_roots = _node_to_roots([a, b, c])
    assert node_to_roots[a.dag_hash()] == frozenset([a.dag_hash()])
    assert node_to_roots[b.dag_hash()] == frozenset([a.dag_hash(), b.dag_hash()])
    assert node_to_roots[c.dag_hash()] == frozenset([c.dag_hash()])
    assert node_to_roots[d.dag_hash()] == frozenset([c.dag_hash()])


def test_nodes_to_roots_shared_dependency():
    """A dependency shared by two roots is attributed to both."""
    specs = create_dag(nodes=["A", "B", "C"], edges=[("A", "C", "all"), ("B", "C", "all")])
    a, b, c = specs["A"], specs["B"], specs["C"]
    node_to_roots = _node_to_roots([a, b])
    assert node_to_roots[a.dag_hash()] == frozenset([a.dag_hash()])
    assert node_to_roots[b.dag_hash()] == frozenset([b.dag_hash()])
    assert node_to_roots[c.dag_hash()] == frozenset([a.dag_hash(), b.dag_hash()])
