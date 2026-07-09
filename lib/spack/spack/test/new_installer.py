# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for the new_installer.py module"""

import json
import os
import pathlib
import signal
import socket
import sys
import time
from typing import Callable, Dict, List, NamedTuple, Optional, Sequence, Set, Tuple, Union

import pytest

import spack.config
import spack.deptypes as dt
import spack.error
import spack.spec
import spack.store
from spack.database import Database
from spack.new_installer import (
    OVERWRITE_GARBAGE_SUFFIX,
    BinaryCacheMiss,
    BuildGraph,
    BuildRequest,
    ChangeJobs,
    ChildInfo,
    ExitCode,
    InstallerUI,
    PackageInstaller,
    PrefixPivoter,
    ScheduleResult,
    SetEcho,
    _node_to_roots,
    create_build_channels,
    read_connection,
    schedule_builds,
    write_connection,
)
from spack.new_installer_base import (
    BuildChannels,
    JobServerBase,
    NoopJobServer,
    ProcessExitNotifier,
)
from spack.test.conftest import writable
from spack.test.traverse import create_dag

if sys.platform != "win32":
    from spack.new_installer_posix import PosixJobServer


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

    def test_no_binary_mirrors_forces_source_only(
        self, temporary_store, mock_packages, mutable_config
    ):
        """With no binary mirrors configured, has_mirrors is False so auto resolves to
        source_only at scheduling time."""
        spec = spack.spec.Spec("trivial-install-test-package")
        spec._mark_concrete()
        installer = PackageInstaller([spec.package], root_policy="auto")
        assert not installer.has_mirrors

    def test_no_binary_mirrors_preserves_cache_only(
        self, temporary_store, mock_packages, mutable_config
    ):
        """Without binary mirrors, an explicit cache_only shouldn't turn into source_only."""
        spec = spack.spec.Spec("trivial-install-test-package")
        spec._mark_concrete()
        installer = PackageInstaller(
            [spec.package], root_policy="cache_only", dependencies_policy="cache_only"
        )
        assert installer.root_policy == "cache_only"
        assert installer.dependencies_policy == "cache_only"


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


def _schedule(
    pending: List[str],
    build_graph,
    store,
    jobserver: Optional[JobServerBase] = None,
    overwrite: Optional[Set[str]] = None,
    overwrite_time: float = 0.0,
    capacity: int = 2,
    needs_jobserver_token: bool = False,
    explicit: Optional[Set[str]] = None,
) -> ScheduleResult:
    """Call schedule_builds() with inert defaults, so tests spell out only what they are about."""
    return schedule_builds(
        pending,
        build_graph,
        store,
        overwrite=overwrite or set(),
        overwrite_time=overwrite_time,
        capacity=capacity,
        needs_jobserver_token=needs_jobserver_token,
        jobserver=jobserver or NoopJobServer(num_jobs=2),
        explicit=explicit or set(),
    )


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
        result = _schedule(pending, _FakeBuildGraph([spec]), temporary_store)
        assert not result.blocked
        assert len(result.to_start) == 1
        assert result.to_start[0][0] == spec.dag_hash()
        assert not result.newly_installed
        assert not pending  # removed from the pending list
        for _, lock in result.to_start:
            lock.release_write()

    def test_already_installed_yields_newly_installed(self, temporary_store, mock_packages):
        """A spec already in the DB is returned in newly_installed, not in to_start."""
        spec = self._make_spec("trivial-install-test-package")
        self._mark_installed(spec, temporary_store)
        pending = [spec.dag_hash()]
        result = _schedule(pending, _FakeBuildGraph([spec]), temporary_store)
        assert not result.blocked
        assert not result.to_start
        assert len(result.newly_installed) == 1
        assert result.newly_installed[0][0] == spec.dag_hash()
        assert not pending  # removed from the pending list
        for _, _, lock in result.newly_installed:
            lock.release_read()

    @pytest.mark.not_on_windows("Windows has no POSIX jobserver, only NoopJobServer")
    def test_no_jobserver_token_returns_empty(self, temporary_store, mock_packages):
        """When has_running_builds=True and no token is available, nothing is started."""
        spec = self._make_spec("trivial-install-test-package")
        pending = [spec.dag_hash()]
        # num_jobs=1 writes 0 tokens to the FIFO. Only the implicit token exists.
        jobserver = PosixJobServer(num_jobs=1, makeflags="")
        try:
            result = _schedule(
                pending,
                _FakeBuildGraph([spec]),
                temporary_store,
                jobserver=jobserver,
                needs_jobserver_token=True,
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
        # Pre-register the lock in the prefix_locker cache, then patch try_acquire to fail.
        lock = temporary_store.prefix_locker.lock(spec)
        monkeypatch.setattr(lock, "try_acquire_write", lambda: False)
        monkeypatch.setattr(lock, "try_acquire_read", lambda: False)
        result = _schedule(pending, _FakeBuildGraph([spec]), temporary_store)
        assert result.blocked
        assert not result.to_start
        assert not result.newly_installed
        assert len(pending) == 1

    def test_overwrite_installed_spec_is_started(self, temporary_store, mock_packages):
        """A spec in the overwrite set is scheduled even when already installed."""
        spec = self._make_spec("trivial-install-test-package")
        self._mark_installed(spec, temporary_store)
        pending = [spec.dag_hash()]
        result = _schedule(
            pending,
            _FakeBuildGraph([spec]),
            temporary_store,
            overwrite={spec.dag_hash()},
            overwrite_time=time.time() + 100,
        )
        assert not result.blocked
        assert len(result.to_start) == 1
        assert result.to_start[0][0] == spec.dag_hash()
        assert not result.newly_installed
        for _, lock in result.to_start:
            lock.release_write()

    def test_mixed_locked_unlocked(self, temporary_store, mock_packages, monkeypatch):
        """Only the unlocked spec enters to_start when one spec is externally locked."""
        spec_a = self._make_spec("trivial-install-test-package")
        spec_b = self._make_spec("trivial-smoke-test")
        pending = [spec_a.dag_hash(), spec_b.dag_hash()]
        # Patch spec_a's lock to always fail, simulating an external write lock.
        lock_a = temporary_store.prefix_locker.lock(spec_a)
        monkeypatch.setattr(lock_a, "try_acquire_write", lambda: False)
        monkeypatch.setattr(lock_a, "try_acquire_read", lambda: False)
        result = _schedule(pending, _FakeBuildGraph([spec_a, spec_b]), temporary_store)
        assert not result.blocked  # spec_b was schedulable
        started_hashes = {h for h, _ in result.to_start}
        assert spec_b.dag_hash() in started_hashes
        assert spec_a.dag_hash() not in started_hashes
        assert not result.newly_installed
        for _, lock in result.to_start:
            lock.release_write()

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
        lock = temporary_store.prefix_locker.lock(spec)
        monkeypatch.setattr(lock, "try_acquire_write", lambda: False)
        result = _schedule(pending, _FakeBuildGraph([spec]), temporary_store)
        assert result.blocked  # no write lock was obtained; jobserver should not fire
        assert not result.to_start
        assert len(result.newly_installed) == 1
        dag_hash, installed_spec, lock = result.newly_installed[0]
        assert dag_hash == spec.dag_hash()
        assert installed_spec == spec
        assert not pending  # spec was removed from pending
        lock.release_read()

    def test_write_locked_read_locked_not_installed_still_blocked(
        self, temporary_store, mock_packages, monkeypatch
    ):
        """Write lock fails, read lock succeeds, but spec is not in DB: retry later.

        Simulates the case where a concurrent process was killed mid-build. The read lock is
        released and the spec stays in pending; blocked should remain True.
        """
        spec = self._make_spec("trivial-install-test-package")
        pending = [spec.dag_hash()]
        lock = temporary_store.prefix_locker.lock(spec)
        monkeypatch.setattr(lock, "try_acquire_write", lambda: False)
        result = _schedule(pending, _FakeBuildGraph([spec]), temporary_store)
        assert result.blocked
        assert not result.to_start
        assert not result.newly_installed
        assert pending == [spec.dag_hash()]  # spec stays in pending for retry

    def test_overwrite_handled_by_concurrent_process(self, temporary_store, mock_packages):
        """When a spec in overwrite was installed AFTER overwrite_time, another process did it."""
        spec = self._make_spec("trivial-install-test-package")
        self._mark_installed(spec, temporary_store)  # installation_time = now()
        pending = [spec.dag_hash()]
        # the default overwrite_time=0.0 is earlier than now()
        result = _schedule(
            pending, _FakeBuildGraph([spec]), temporary_store, overwrite={spec.dag_hash()}
        )
        assert not result.blocked
        assert not result.to_start
        assert len(result.newly_installed) == 1
        assert result.newly_installed[0][0] == spec.dag_hash()
        for _, _, lock in result.newly_installed:
            lock.release_read()

    def test_installed_implicit_explicit_set_produces_db_update(
        self, temporary_store, mock_packages
    ):
        """An installed-implicit spec in explicit set produces a DbUpdate."""
        spec = self._make_spec("trivial-install-test-package")
        temporary_store.layout.create_install_directory(spec)
        temporary_store.db.add(spec, explicit=False)
        pending = [spec.dag_hash()]
        result = _schedule(
            pending, _FakeBuildGraph([spec]), temporary_store, explicit={spec.dag_hash()}
        )
        assert len(result.to_mark_explicit) == 1
        assert result.to_mark_explicit[0].spec is spec
        assert len(result.newly_installed) == 1
        for _, _, lock in result.newly_installed:
            lock.release_read()

    def test_missing_in_upstream_is_installed_locally(
        self, upstream_and_downstream_db: Tuple[Database, Database], mock_packages
    ):
        """A spec that is referenced but not installed in an upstream database is scheduled for
        a local build, with its prefix repointed to the local store."""
        upstream_db, downstream_db = upstream_and_downstream_db
        dep = self._make_spec("dependency-install")
        parent = spack.spec.Spec("dependent-install")
        parent._add_dependency(dep, depflag=dt.BUILD, virtuals=())
        parent._mark_concrete()

        # Register both specs in the upstream, then uninstall the dep: its record is kept as
        # uninstalled because the parent still references it.
        with writable(upstream_db):
            upstream_db.add(parent, explicit=True)
            upstream_db.remove(dep)

        # Create a Store for schedule_builds based on the downstream database.
        local_store = spack.store.Store(downstream_db.root, upstreams=[upstream_db])
        upstream, record = local_store.db.query_by_spec_hash(dep.dag_hash())
        assert upstream and record is not None and not record.installed

        # Like BuildGraph, start out with the prefix from the upstream record.
        assert upstream_db.layout
        dep.set_prefix(upstream_db.layout.path_for_spec(dep))

        result = _schedule([dep.dag_hash()], _FakeBuildGraph([dep]), local_store)
        assert not result.blocked
        assert [dag_hash for dag_hash, _ in result.to_start] == [dep.dag_hash()]
        # The prefix was repointed from the upstream to the local store.
        assert dep.prefix == local_store.layout.path_for_spec(dep)

        # Cleanup
        for _, lock in result.to_start:
            lock.release_write()

    def test_overwrite_prefix_mismatch_raises(self, temporary_store, mock_packages):
        """An overwrite install cannot proceed when the spec prefix differs from the DB path."""
        spec = self._make_spec("trivial-install-test-package")
        self._mark_installed(spec, temporary_store)
        spec.set_prefix("/some/other/prefix")
        with pytest.raises(spack.error.InstallError, match="Prefix mismatch in overwrite"):
            _schedule(
                [spec.dag_hash()],
                _FakeBuildGraph([spec]),
                temporary_store,
                overwrite={spec.dag_hash()},
                overwrite_time=time.time() + 100,
            )

    def test_prefix_collision_raises(self, temporary_store, mock_packages):
        """A spec cannot be scheduled into a prefix already occupied by another spec."""
        installed = self._make_spec("trivial-install-test-package")
        self._mark_installed(installed, temporary_store)
        colliding = self._make_spec("trivial-smoke-test")
        colliding.set_prefix(temporary_store.layout.path_for_spec(installed))
        with pytest.raises(spack.error.InstallError, match="already exists"):
            _schedule([colliding.dag_hash()], _FakeBuildGraph([colliding]), temporary_store)


class RecordingUI(InstallerUI):
    """Frontend that records the events it receives, for testing the event loop."""

    def __init__(self) -> None:
        super().__init__()
        self.events: List[tuple] = []

    def on_build_added(self, info):
        self.events.append(("build_added", info.id, info.name))

    def on_build_removed(self, build_id):
        self.events.append(("build_removed", build_id))

    def on_state_changed(self, build_id, state):
        self.events.append(("state_changed", build_id, state))

    def on_log_output(self, build_id, data):
        self.events.append(("log_output", build_id, data))

    def on_total_increased(self, count):
        self.events.append(("total_increased", count))

    def on_progress(self, build_id, current, total):
        self.events.append(("progress", build_id, current, total))

    def on_jobs_changed(self, actual, target):
        self.events.append(("jobs_changed", actual, target))

    def on_finished(self, failures):
        self.events.append(("finished", tuple(failures)))


class DrivingUI(RecordingUI):
    """Records events and runs a callback on every event-loop tick, so tests can finish hanging
    builds from inside install()."""

    def __init__(self, on_tick: Callable[[], None]) -> None:
        super().__init__()
        self.on_tick = on_tick

    def refresh_interval(self) -> float:
        return 0.01

    def render(self, finalize: bool = False) -> None:
        if not finalize:
            self.on_tick()


class Script(NamedTuple):
    """The scripted result of a single launched build."""

    exitcode: int = ExitCode.SUCCESS
    states: Tuple[str, ...] = ()
    output: bytes = b""
    #: Raw bytes written to the state channel verbatim, for protocol edge cases.
    raw_state: bytes = b""
    #: Keep the build running until the test calls finish() or the event loop terminates it.
    hang: bool = False


class FakeBuild(ProcessExitNotifier):
    """A ``ProcessLike`` for builds that run in-process, without forking. It stays alive until
    finish() or terminate() is called (immediately at launch for non-hanging scripts). Doubles as
    its own exit notifier: a socketpair (selectable on Windows too, like the production
    WindowsSentinelBridge) whose write end is closed when the build finishes."""

    #: There is no real process (group) to signal.
    pid: Optional[int] = None

    def __init__(self, exitcode: int, channels: BuildChannels) -> None:
        self._read, self._write = socket.socketpair()
        self._exitcode = exitcode
        self.exitcode: Optional[int] = None
        self.terminated = False
        self.channels = channels

    @property
    def fileobj(self) -> socket.socket:
        return self._read

    def close(self) -> None:
        # The event loop closes this object as notifier and as process; socket.close() is
        # idempotent, so that is fine.
        self._read.close()

    def finish(self) -> None:
        if self.exitcode is None:
            self.exitcode = self._exitcode
            # EOF the state/output channels and make the exit notifier fire.
            self.channels.state_w.close()
            self.channels.output_w.close()
            self._write.close()

    def terminate(self) -> None:
        self.terminated, self._exitcode = True, -signal.SIGTERM
        self.finish()

    kill = terminate

    def is_alive(self) -> bool:
        return self.exitcode is None

    def join(self, timeout: Optional[float] = None) -> None:
        pass


class ScriptedLauncher:
    """Build launcher that runs builds in-process with scripted state messages, output and exit
    code. A list of scripts is consumed one per launch, so retries (e.g. after a binary cache
    miss) can behave differently per attempt."""

    def __init__(self, scripts: Dict[str, Union[Script, List[Script]]]) -> None:
        self.scripts = {
            name: [s] if isinstance(s, Script) else list(s) for name, s in scripts.items()
        }
        self.requests: List[BuildRequest] = []
        #: All launched builds, in launch order, for tests to inspect.
        self.builds: List[FakeBuild] = []
        #: The subset of launched builds that hang, for tests to finish() or inspect.
        self.hanging: List[FakeBuild] = []

    def __call__(self, request: BuildRequest, jobserver: JobServerBase) -> ChildInfo:
        self.requests.append(request)
        script = self.scripts[request.spec.name].pop(0)
        channels = create_build_channels()
        for state in script.states:
            write_connection(channels.state_w, json.dumps({"state": state}).encode() + b"\n")
        if script.raw_state:
            write_connection(channels.state_w, script.raw_state)
        if script.output:
            write_connection(channels.output_w, script.output)
        build = FakeBuild(script.exitcode, channels)
        self.builds.append(build)
        if script.hang:
            # The channels stay open until the test finishes the build.
            self.hanging.append(build)
        else:
            # Finishing EOFs the channels and the exit notifier, like a child that exited.
            build.finish()
        return ChildInfo(
            build,
            request.spec,
            channels.output_r,
            channels.state_r,
            channels.control_w,
            build,
            request.log_path,
        )


def _make_concrete(
    name: str, deps: Sequence[spack.spec.Spec] = (), depflag: dt.DepFlag = dt.BUILD | dt.LINK
) -> spack.spec.Spec:
    spec = spack.spec.Spec(f"{name}@=1.0")
    for dep in deps:
        spec._add_dependency(dep, depflag=depflag, virtuals=())
    spec._mark_concrete()
    return spec


def _record(store, spec: spack.spec.Spec):
    """The spec's InstallRecord, or None if it is not in the database."""
    return store.db.query_by_spec_hash(spec.dag_hash())[1]


def _install(launcher, *specs: spack.spec.Spec, ui=None, **kwargs) -> RecordingUI:
    """Install specs through the event loop with a scripted launcher; explicit by default."""
    ui = ui or RecordingUI()
    PackageInstaller(
        [s.package for s in specs], explicit=True, ui=ui, launcher=launcher, **kwargs
    ).install()
    return ui


@pytest.mark.disable_clean_stage_check  # failed builds keep their log file in the stage root
def test_build_failure_reported_through_event_loop(temporary_store, mock_packages):
    """A build exiting with an error yields exactly one failed event, an InstallError naming the
    log file, and no database record -- without forking any build process."""
    spec = _make_concrete("trivial-install-test-package")
    launcher = ScriptedLauncher({spec.name: Script(exitcode=ExitCode.BUILD_ERROR)})
    ui = RecordingUI()
    installer = PackageInstaller([spec.package], explicit=True, ui=ui, launcher=launcher)

    with pytest.raises(spack.error.InstallError) as exc_info:
        installer.install()

    dag_hash = spec.dag_hash()
    assert installer.log_paths[dag_hash] in str(exc_info.value)
    failed = [e for e in ui.events if e[0] == "state_changed" and e[2] == "failed"]
    assert failed == [("state_changed", dag_hash, "failed")]
    assert _record(temporary_store, spec) is None


def test_cache_miss_falls_back_to_source_build(
    temporary_store, mock_packages, mutable_config, tmp_path
):
    """With a binary mirror configured, the first attempt is cache_only; a cache miss removes the
    build from the UI, reschedules it as source_only, and the second attempt succeeds."""
    spack.config.set("mirrors", {"local": {"url": (tmp_path / "mirror").as_uri(), "binary": True}})
    spec = _make_concrete("trivial-install-test-package")
    launcher = ScriptedLauncher(
        {spec.name: [Script(exitcode=ExitCode.BUILD_CACHE_MISS), Script(exitcode=0)]}
    )
    ui = _install(launcher, spec)

    assert [r.install_policy for r in launcher.requests] == ["cache_only", "source_only"]

    dag_hash = spec.dag_hash()
    lifecycle = [e[0] for e in ui.events if e[1] == dag_hash and e[0] != "state_changed"]
    assert lifecycle == ["build_added", "build_removed", "build_added"]
    assert ("state_changed", dag_hash, "finished") in ui.events
    record = _record(temporary_store, spec)
    assert record is not None and record.explicit


def test_build_output_streams_to_frontend(temporary_store, mock_packages):
    """Output and state messages written by a build arrive at the frontend as log_output and
    state_changed events, byte for byte and in order."""
    payload = b"checking for compiler...\nbuilding...\n"
    spec = _make_concrete("trivial-install-test-package")
    launcher = ScriptedLauncher({spec.name: Script(states=("staging",), output=payload)})
    ui = _install(launcher, spec)

    dag_hash = spec.dag_hash()
    received = b"".join(e[2] for e in ui.events if e[0] == "log_output" and e[1] == dag_hash)
    assert received == payload
    assert ("state_changed", dag_hash, "staging") in ui.events
    assert ("state_changed", dag_hash, "finished") in ui.events


def test_package_installer_with_injected_ui(temporary_store, mock_packages):
    """The event loop runs against a custom InstallerUI frontend without any terminal code.

    Uses the mark-explicit path (spec installed implicitly, requested explicitly) so the loop
    schedules, reports, and persists to the database without spawning build processes."""
    spec = _make_concrete("trivial-install-test-package")
    temporary_store.layout.create_install_directory(spec)
    temporary_store.db.add(spec, explicit=False)

    ui = _install(None, spec)

    dag_hash = spec.dag_hash()
    assert ("build_added", dag_hash, spec.name) in ui.events
    assert ("state_changed", dag_hash, "finished") in ui.events

    # The spec was marked explicit in the database.
    record = _record(temporary_store, spec)
    assert record is not None and record.explicit


def test_dependency_built_before_dependent(temporary_store, mock_packages):
    """Builds are launched in dependency order and both land in the database."""
    dep = _make_concrete("dependency-install")
    root = _make_concrete("dependent-install", deps=[dep])
    launcher = ScriptedLauncher({dep.name: Script(), root.name: Script()})
    _install(launcher, root)

    assert [r.spec.name for r in launcher.requests] == [dep.name, root.name]
    assert _record(temporary_store, dep) and _record(temporary_store, root)


def test_capacity_serializes_launches(temporary_store, mock_packages):
    """With concurrent_packages=1 the second build is only requested after the first finished."""
    a, b = _make_concrete("pkg-a"), _make_concrete("pkg-b")
    launcher = ScriptedLauncher({a.name: Script(hang=True), b.name: Script(hang=True)})
    requests_at_finish = []

    def tick():
        if launcher.hanging:
            requests_at_finish.append(len(launcher.requests))
            launcher.hanging.pop(0).finish()

    _install(launcher, a, b, ui=DrivingUI(tick), concurrent_packages=1)

    assert requests_at_finish == [1, 2]


def test_stopped_at_phase_is_not_a_failure(temporary_store, mock_packages):
    """A build exiting with STOPPED_AT_PHASE raises nothing, reports no failure, and leaves no
    database record."""
    spec = _make_concrete("trivial-install-test-package")
    launcher = ScriptedLauncher({spec.name: Script(exitcode=ExitCode.STOPPED_AT_PHASE)})
    ui = _install(launcher, spec)

    assert not [e for e in ui.events if e[0] == "state_changed" and e[2] == "failed"]
    assert _record(temporary_store, spec) is None


@pytest.mark.disable_clean_stage_check  # failed builds keep their log file in the stage root
def test_fail_fast_terminates_running_builds(temporary_store, mock_packages):
    """In fail_fast mode a failure terminates the still-running build, which is not itself
    reported as a failure."""
    bad, hanging = _make_concrete("pkg-a"), _make_concrete("pkg-b")
    launcher = ScriptedLauncher(
        {bad.name: Script(exitcode=ExitCode.BUILD_ERROR), hanging.name: Script(hang=True)}
    )
    ui = RecordingUI()
    with pytest.raises(spack.error.InstallError) as exc_info:
        _install(launcher, bad, hanging, ui=ui, fail_fast=True, concurrent_packages=2)

    assert launcher.hanging[0].terminated
    failed = [e for e in ui.events if e[0] == "state_changed" and e[2] == "failed"]
    assert failed == [("state_changed", bad.dag_hash(), "failed")]
    assert bad.name in str(exc_info.value) and hanging.name not in str(exc_info.value)


def test_set_echo_commands_reach_control_channel(temporary_store, mock_packages):
    """SetEcho commands queued by the UI are written as b"1"/b"0" to the control channel of the
    build, which is still registered as running when the command queue is drained."""
    spec = _make_concrete("trivial-install-test-package")
    launcher = ScriptedLauncher({spec.name: Script()})
    ui = RecordingUI()
    ui.commands += [SetEcho(spec.dag_hash(), True), SetEcho(spec.dag_hash(), False)]
    _install(launcher, spec, ui=ui)

    assert read_connection(launcher.builds[0].channels.control_r, 16) == b"10"


def test_cache_miss_expands_build_deps(temporary_store, mock_packages, mutable_config, tmp_path):
    """A cache miss on a root with unexpanded build deps schedules those deps (growing the UI
    total) and retries the root as source_only."""
    spack.config.set("mirrors", {"local": {"url": (tmp_path / "mirror").as_uri(), "binary": True}})
    dep = _make_concrete("dependency-install")
    root = _make_concrete("dependent-install", deps=[dep], depflag=dt.BUILD)
    launcher = ScriptedLauncher(
        {root.name: [Script(exitcode=ExitCode.BUILD_CACHE_MISS), Script()], dep.name: Script()}
    )
    ui = _install(launcher, root)

    assert [(r.spec.name, r.install_policy) for r in launcher.requests] == [
        (root.name, "cache_only"),
        (dep.name, "cache_only"),
        (root.name, "source_only"),
    ]
    assert ("total_increased", 1) in ui.events
    assert _record(temporary_store, dep) and _record(temporary_store, root)


def test_external_spec_uses_devnull_log(temporary_store, mock_packages):
    """External specs get os.devnull as log path and are recorded in the database."""
    spec = _make_concrete("trivial-install-test-package")
    spec.external_path = "/usr"
    launcher = ScriptedLauncher({spec.name: Script()})
    _install(launcher, spec)

    assert launcher.requests[0].log_path == os.devnull
    record = _record(temporary_store, spec)
    assert record is not None and record.installed


def test_overwrite_reinstalls_through_event_loop(temporary_store, mock_packages):
    """An overwrite install of an already-installed spec launches a build and refreshes the
    database record."""
    spec = _make_concrete("trivial-install-test-package")
    temporary_store.layout.create_install_directory(spec)
    temporary_store.db.add(spec, explicit=True)
    old_time = _record(temporary_store, spec).installation_time

    launcher = ScriptedLauncher({spec.name: Script()})
    _install(launcher, spec, overwrite=[spec.dag_hash()])

    assert len(launcher.requests) == 1
    assert _record(temporary_store, spec).installation_time > old_time


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


def test_expand_build_deps_source_only_includes_nested_build_deps(temporary_store):
    """When dependencies_policy is source_only, expand_build_deps must include BUILD deps of
    dynamically added specs, not just LINK|RUN. Otherwise those specs attempt to build from source
    without their build tools in the graph."""
    # root --[build]--> build_tool --[build]--> nested_build_tool
    #                              --[link]-->  lib_dep
    specs = create_dag(
        nodes=["root", "build_tool", "nested_build_tool", "lib_dep"],
        edges=[
            ("root", "build_tool", "build"),
            ("build_tool", "nested_build_tool", "build"),
            ("build_tool", "lib_dep", "link"),
        ],
    )
    root = specs["root"]
    for s in specs.values():
        s._mark_concrete()

    # Construct a BuildGraph with root_policy="auto" so root's build deps are deferred.
    build_graph = BuildGraph(
        specs=[root],
        root_policy="auto",
        dependencies_policy="source_only",
        include_build_deps=False,
        install_package=True,
        install_deps=True,
        store=temporary_store,
    )

    # The initial graph should contain only root (build deps deferred for "auto" policy).
    assert root.dag_hash() in build_graph.nodes
    assert specs["build_tool"].dag_hash() not in build_graph.nodes

    # Simulate a cache miss: expand build deps for root.
    pending = []
    with temporary_store.db.read_transaction():
        newly_added = build_graph.expand_build_deps(
            [root.dag_hash()], pending, temporary_store.db, dependencies_policy="source_only"
        )

    added_hashes = set(newly_added)

    # build_tool must be added (direct BUILD dep of root)
    assert specs["build_tool"].dag_hash() in added_hashes

    # lib_dep must be added (LINK dep of build_tool)
    assert specs["lib_dep"].dag_hash() in added_hashes

    # nested_build_tool must also be added (BUILD dep of build_tool). This is the bug: without the
    # fix, expand_build_deps only traverses LINK|RUN, so nested_build_tool is missing.
    assert specs["nested_build_tool"].dag_hash() in added_hashes


def test_installed_from_binary_cache_message_sets_package_attr(temporary_store, mock_packages):
    """The installed_from_binary_cache state message sets the corresponding package attribute in
    the parent process."""
    spec = _make_concrete("trivial-install-test-package")
    launcher = ScriptedLauncher(
        {spec.name: Script(raw_state=b'{"installed_from_binary_cache":true}\n')}
    )
    _install(launcher, spec)

    assert spec.package.installed_from_binary_cache is True


def test_state_messages_tolerate_garbage_and_partial_lines(temporary_store, mock_packages):
    """Empty and non-JSON state lines are skipped, and a message split across two writes is
    reassembled from the per-build state buffer."""
    spec = _make_concrete("trivial-install-test-package")
    launcher = ScriptedLauncher({spec.name: Script(raw_state=b'garbage\n\n{"sta', hang=True)})

    def tick():
        if launcher.hanging:
            # The first chunk was consumed before the first tick; complete the partial line.
            proc = launcher.hanging.pop(0)
            write_connection(proc.channels.state_w, b'te":"staging"}\n')
            proc.finish()

    ui = _install(launcher, spec, ui=DrivingUI(tick))

    dag_hash = spec.dag_hash()
    assert ("state_changed", dag_hash, "staging") in ui.events
    assert ("state_changed", dag_hash, "finished") in ui.events


@pytest.mark.disable_clean_stage_check  # failed builds keep their log file in the stage root
def test_reports_collect_success_failure_and_skips(temporary_store, mock_packages):
    """With create_reports=True, each root gets a RequestRecord: a failed dep is recorded as
    failure, its dependent as skipped, and an independent successful root as success."""
    dep = _make_concrete("dependency-install")
    root = _make_concrete("dependent-install", deps=[dep])
    other = _make_concrete("trivial-install-test-package")
    launcher = ScriptedLauncher(
        {dep.name: Script(exitcode=ExitCode.BUILD_ERROR), other.name: Script()}
    )
    installer = PackageInstaller(
        [root.package, other.package],
        explicit=True,
        ui=RecordingUI(),
        launcher=launcher,
        create_reports=True,
    )
    with pytest.raises(spack.error.InstallError):
        installer.install()

    root_results = {r.name: r.result for r in installer.reports[root.dag_hash()].packages}
    assert root_results == {dep.name: "failure", root.name: "skipped"}
    root_record = next(
        r for r in installer.reports[root.dag_hash()].packages if r.name == root.name
    )
    assert root_record.message == "Dependencies failed to install"
    assert [r.result for r in installer.reports[other.dag_hash()].packages] == ["success"]


@pytest.mark.disable_clean_stage_check  # interrupted installs keep their log files
def test_keyboard_interrupt_terminates_builds_and_flushes_db(temporary_store, mock_packages):
    """A KeyboardInterrupt from the UI propagates, terminates the running build, and still
    flushes already-finished builds to the database."""
    dep = _make_concrete("dependency-install")
    root = _make_concrete("dependent-install", deps=[dep])
    launcher = ScriptedLauncher({dep.name: Script(), root.name: Script(hang=True)})

    def tick():
        if launcher.hanging:  # the dep finished and the root build is now running
            raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        _install(launcher, root, ui=DrivingUI(tick))

    assert launcher.hanging[0].terminated
    assert _record(temporary_store, dep) is not None
    assert _record(temporary_store, root) is None


@pytest.mark.disable_clean_stage_check  # failed builds keep their log file in the stage root
def test_failed_builds_reach_on_finished(temporary_store, mock_packages):
    """The loop notifies the frontend of the failed build ids before raising InstallError."""
    spec = _make_concrete("trivial-install-test-package")
    launcher = ScriptedLauncher({spec.name: Script(exitcode=ExitCode.BUILD_ERROR)})
    ui = RecordingUI()

    with pytest.raises(spack.error.InstallError):
        _install(launcher, spec, ui=ui)

    assert ("finished", (spec.dag_hash(),)) in ui.events


def test_set_echo_unknown_build_is_noop(temporary_store, mock_packages):
    """A SetEcho command for a build id that is not running does nothing."""
    spec = _make_concrete("trivial-install-test-package")
    launcher = ScriptedLauncher({spec.name: Script()})
    ui = RecordingUI()
    ui.commands.append(SetEcho("0" * 32, True))
    _install(launcher, spec, ui=ui)

    assert _record(temporary_store, spec) is not None


def test_explicit_policies_reach_build_requests(temporary_store, mock_packages):
    """Explicit root/dependencies policies are passed through to the build requests instead of
    being resolved dynamically like "auto"."""
    dep = _make_concrete("dependency-install")
    root = _make_concrete("dependent-install", deps=[dep])
    launcher = ScriptedLauncher({dep.name: Script(), root.name: Script()})
    _install(launcher, root, root_policy="source_only", dependencies_policy="cache_only")

    assert [(r.spec.name, r.install_policy) for r in launcher.requests] == [
        (dep.name, "cache_only"),
        (root.name, "source_only"),
    ]


def test_explicit_as_set_marks_only_those_specs(temporary_store, mock_packages):
    """When explicit is a set of dag hashes, only those specs are marked explicit in the DB."""
    a, b = _make_concrete("pkg-a"), _make_concrete("pkg-b")
    launcher = ScriptedLauncher({a.name: Script(), b.name: Script()})
    PackageInstaller(
        [a.package, b.package], explicit={a.dag_hash()}, ui=RecordingUI(), launcher=launcher
    ).install()

    assert _record(temporary_store, a).explicit
    assert not _record(temporary_store, b).explicit


@pytest.mark.not_on_windows("Windows has no POSIX jobserver, only NoopJobServer")
def test_change_jobs_commands_adjust_parallelism(temporary_store, mock_packages):
    """ChangeJobs commands queued by the UI adjust the jobserver, and the new job counts are
    reported back through jobs_changed events."""
    spec = _make_concrete("trivial-install-test-package")
    launcher = ScriptedLauncher({spec.name: Script()})
    ui = RecordingUI()
    ui.commands += [ChangeJobs(1), ChangeJobs(-1)]
    _install(launcher, spec, ui=ui)

    jobs_events = [e for e in ui.events if e[0] == "jobs_changed"]
    initial = jobs_events[0][2]
    assert ("jobs_changed", initial + 1, initial + 1) in jobs_events
    assert jobs_events[-1][2] == initial  # target restored after the decrease
