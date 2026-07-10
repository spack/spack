# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Parent side of the new installer: the :class:`PackageInstaller` event loop.

Runs the selector-based event loop that starts builds, forwards their output, applies UI
commands, and flushes finished builds to the database. See :mod:`spack.installer` for the
overall design."""

import json
import os
import selectors
import signal
import sys
import tempfile
import time
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Set, Union

import spack.binary_distribution
import spack.config
import spack.deprecation
import spack.error
import spack.mirrors.mirror
import spack.report
import spack.spec
import spack.stage
import spack.store
import spack.traverse
import spack.url_buildcache
import spack.util.filesystem as fs
import spack.util.lock
import spack.util.tty
from spack.installer.base import (
    JOBSERVER_EVENT,
    OUTPUT_BUFFER_SIZE,
    SIGWINCH_EVENT,
    STDIN_EVENT,
    BaseTerminalState,
    ExitCode,
    FdInfo,
    InstallPolicy,
    JobServerBase,
)
from spack.installer.build import BuildRequest, ChildInfo, start_build
from spack.installer.schedule import (
    AddSpecAction,
    BuildGraph,
    DatabaseAction,
    _node_to_roots,
    schedule_builds,
)
from spack.installer.ui import BuildInfo, InstallerUI, SetEcho, TerminalUI

if sys.platform == "win32":
    from spack.installer.base import NoopJobServer as JobServer
    from spack.installer.windows import WindowsTerminalState as TerminalState
    from spack.installer.windows import read_connection, write_connection
else:
    from spack.installer.posix import PosixJobServer as JobServer
    from spack.installer.posix import PosixTerminalState as TerminalState
    from spack.installer.posix import read_connection, write_connection

if TYPE_CHECKING:
    import spack.package_base

#: How often to flush completed builds to the database
DATABASE_WRITE_INTERVAL = 5.0


class ReportData:
    """Data collected for reports during installation."""

    def __init__(self, roots: List[spack.spec.Spec]):
        self.roots = roots
        self.build_records: Dict[str, spack.report.InstallRecord] = {}

    def start_record(self, spec: spack.spec.Spec) -> None:
        """Begin an InstallRecord for a spec that is about to be built."""
        if spec.external:
            return
        record = spack.report.InstallRecord(spec)
        record.start()
        self.build_records[spec.dag_hash()] = record

    def finish_record(
        self, spec: spack.spec.Spec, exitcode: int, log_path: Optional[str] = None
    ) -> None:
        """Mark the InstallRecord for a spec as succeeded or failed."""
        record = self.build_records.get(spec.dag_hash())
        if record is None or spec.external:
            return
        if exitcode == ExitCode.SUCCESS:
            record.succeed(log_path)
        else:
            record.fail(
                spack.error.InstallError(
                    f"Installation of {spec.name} failed; see log for details"
                ),
                log_path,
            )

    def finalize(
        self, reports: Dict[str, spack.report.RequestRecord], build_graph: BuildGraph
    ) -> None:
        """Finalize InstallRecords and append them to RequestRecords after all builds finish.

        Args:
            reports: Map of root dag_hash to RequestRecord to append to.
            build_graph: The build graph containing all nodes and their states.
        """
        node_to_roots = _node_to_roots(self.roots)

        for spec in spack.traverse.traverse_nodes(self.roots):
            h = spec.dag_hash()
            if h in self.build_records:
                record = self.build_records[h]
            else:
                record = spack.report.InstallRecord(spec)
                if spec.external:
                    msg = "Spec is external"
                elif h in build_graph.pruned:
                    msg = "Spec was not scheduled for installation"
                elif h in build_graph.nodes:
                    msg = "Dependencies failed to install"
                else:
                    # If not installed or failed (build_records), not statically pruned ahead of
                    # time (build_graph.pruned), and also not scheduled (build_graph.nodes), it
                    # means it was in pending_builds or running_builds but never started/finished.
                    # This branch is followed on KeyboardInterrupt and --fail-fast.
                    msg = "Installation was interrupted"
                record.skip(msg=msg)

            for root_hash in node_to_roots[h]:
                reports[root_hash].append_record(record)


class NullReportData(ReportData):
    """No-op drop-in for ReportData when no reporter is configured.

    Avoids creating InstallRecords and reading log files on every completed build."""

    def __init__(self) -> None:
        super().__init__(roots=[])

    def start_record(self, spec: spack.spec.Spec) -> None:
        pass

    def finish_record(
        self, spec: spack.spec.Spec, exitcode: int, log_path: Optional[str] = None
    ) -> None:
        pass

    def finalize(
        self, reports: Dict[str, spack.report.RequestRecord], build_graph: "BuildGraph"
    ) -> None:
        pass


def _signal_children(running_builds: Dict[str, ChildInfo], sig: signal.Signals) -> None:
    """Send a signal to the process group of each running build."""
    for child in running_builds.values():
        try:
            pid = child.proc.pid
            if pid is not None:
                os.killpg(pid, sig)
        except OSError:
            pass


class PackageInstaller:
    explicit: Set[str]

    def __init__(
        self,
        packages: List["spack.package_base.PackageBase"],
        *,
        dirty: bool = False,
        explicit: Union[Set[str], bool] = False,
        overwrite: Optional[Union[List[str], Set[str]]] = None,
        fail_fast: bool = False,
        fake: bool = False,
        include_build_deps: bool = False,
        install_deps: bool = True,
        install_package: bool = True,
        install_source: bool = False,
        keep_prefix: bool = False,
        keep_stage: bool = False,
        restage: bool = True,
        skip_patch: bool = False,
        stop_at: Optional[str] = None,
        stop_before: Optional[str] = None,
        tests: Union[bool, List[str], Set[str]] = False,
        unsigned: Optional[bool] = None,
        verbose: bool = False,
        show_log_on_error: bool = False,
        concurrent_packages: Optional[int] = None,
        root_policy: InstallPolicy = "auto",
        dependencies_policy: InstallPolicy = "auto",
        create_reports: bool = False,
        ui: Optional[InstallerUI] = None,
        launcher: Callable[[BuildRequest, JobServerBase], ChildInfo] = start_build,
        store: Optional[spack.store.Store] = None,
    ) -> None:
        assert install_package or install_deps, "Must install package, dependencies or both"

        self.install_source = install_source
        self.stop_at = stop_at
        self.stop_before = stop_before
        self.tests: Union[bool, List[str], Set[str]] = tests

        self.store = store or spack.store.STORE

        specs = [pkg.spec for pkg in packages]

        self.roots = specs
        self.has_mirrors = bool(spack.mirrors.mirror.MirrorCollection(binary=True))
        self.root_policy: InstallPolicy = root_policy
        self.dependencies_policy: InstallPolicy = dependencies_policy
        self.include_build_deps = include_build_deps
        #: Set of DAG hashes to overwrite (if already installed)
        self.overwrite: Set[str] = set(overwrite) if overwrite else set()
        #: Time at which the overwrite install was requested; used to detect concurrent overwrites.
        self.overwrite_time: float = time.time()
        self.keep_prefix = keep_prefix
        self.fail_fast = fail_fast

        if explicit is True:
            self.explicit = {spec.dag_hash() for spec in specs}
        elif explicit is False:
            self.explicit = set()
        else:
            self.explicit = explicit

        # Build the dependency graph
        self.build_graph = BuildGraph(
            specs,
            root_policy,
            dependencies_policy,
            include_build_deps,
            install_package,
            install_deps,
            self.store,
            self.overwrite,
            tests,
            self.explicit,
            self.has_mirrors,
        )

        #: Per-spec buildcache mirrors; populated in install() from the binary index.
        self.binary_cache_for_spec: Dict[str, List[spack.url_buildcache.MirrorMetadata]] = {}
        self.unsigned = unsigned
        self.dirty = dirty
        self.fake = fake
        self.launcher = launcher
        self.restage = restage
        self.keep_stage = keep_stage
        self.skip_patch = skip_patch

        #: queue of packages ready to install (no children)
        self.pending_builds = [
            parent for parent, children in self.build_graph.parent_to_child.items() if not children
        ]

        #: specs awaiting build-dep expansion (deferred until DB read lock is available)
        self.pending_expansions: List[str] = []

        self.verbose = verbose
        self.running_builds: Dict[str, ChildInfo] = {}
        self.log_paths: Dict[str, str] = {}
        self.ui = ui or TerminalUI(
            total=0,
            verbose=verbose,
            filter_padding=self.store.has_padding(),
            show_log_on_error=show_log_on_error,
        )
        self.ui.on_total_increased(len(self.build_graph.nodes))
        self.jobs = spack.config.determine_number_of_jobs(parallel=True)
        self.ui.on_jobs_changed(self.jobs, self.jobs)
        if concurrent_packages is None:
            concurrent_packages_config = spack.config.CONFIG.get("config:concurrent_packages", 0)
            # The value 0 in config means no limit (other than self.jobs)
            if concurrent_packages_config == 0:
                self.capacity = sys.maxsize
            else:
                self.capacity = concurrent_packages_config
        else:
            self.capacity = concurrent_packages

        # The reports property is what the old installer has and used as public interface.
        if create_reports:
            self.reports = {spec.dag_hash(): spack.report.RequestRecord(spec) for spec in specs}
            self.report_data = ReportData(specs)
        else:
            self.reports = {}
            self.report_data = NullReportData()

        self.next_database_write = 0.0

    def install(self) -> None:
        # check what specs we could fetch from binaries (checks against cache, not remotely)
        try:
            spack.binary_distribution.BINARY_INDEX.update()
        except spack.binary_distribution.FetchCacheError:
            pass

        self.binary_cache_for_spec = {
            s.dag_hash(): spack.binary_distribution.BINARY_INDEX.find_by_hash(
                s.build_spec.dag_hash()
            )
            for s in self.build_graph.nodes.values()
        }

        self._run_event_loop()

    def _run_event_loop(self) -> None:
        spack.deprecation.check_deprecations(self.roots)
        self.store.install_sbang()
        jobserver = JobServer(self.jobs, os.environ.get("MAKEFLAGS", ""))
        selector = selectors.DefaultSelector()

        # Terminal handling (cbreak, suspend/resume signals, stdin registration) is event loop
        # plumbing, enabled only for frontends that read the controlling terminal.
        terminal: Optional[BaseTerminalState] = None
        if self.ui.reads_terminal_input and TerminalState.stdin_is_interactive():
            terminal = TerminalState(
                selector,
                on_headless=self.ui.on_headless_changed,
                on_suspend=lambda: _signal_children(self.running_builds, signal.SIGSTOP),
                on_resume=lambda: _signal_children(self.running_builds, signal.SIGCONT),
            )
            terminal.setup()

        # Finished builds that have not yet been written to the database.
        database_actions: List[DatabaseAction] = []
        # Prefix read locks retained after DB flush (downgraded from write locks in _save_to_db).
        retained_read_locks: List[spack.util.lock.Lock] = []

        failures: List[spack.spec.Spec] = []
        finished_builds: List[str] = []

        try:
            # Try to schedule builds immediately. The first job does not require a token.
            blocked = False
            if self.pending_builds:
                blocked = self._schedule_builds(
                    selector, jobserver, retained_read_locks, database_actions
                )
                self._run_ui_commands(jobserver)
                self._flush_db_if_due(time.monotonic(), database_actions, retained_read_locks)

            while (
                self.pending_builds
                or self.running_builds
                or database_actions
                or self.pending_expansions
            ):
                # Monitor the jobserver when we have pending builds, capacity, and at least one
                # spec is not locked by another process. Also listen if the target parallelism is
                # reduced.
                wake_on_jobserver = bool(
                    self.pending_builds
                    and self.capacity
                    and not blocked
                    or not jobserver.has_target_parallelism()
                )
                jobserver.update_selector(selector, wake_on_jobserver)

                stdin_ready = False

                # How long the loop may sleep, bounded by whichever owner needs attention soonest:
                # the frontend's redraw cadence (UI-owned), the database flush interval
                # (loop-owned), and, while backgrounded, a poll for the foreground transition
                # (terminal-owned).
                timeout = DATABASE_WRITE_INTERVAL
                refresh_interval = self.ui.refresh_interval()
                if refresh_interval is not None:
                    timeout = min(timeout, refresh_interval)
                wake_interval = terminal.wake_interval() if terminal is not None else None
                if wake_interval is not None:
                    timeout = min(timeout, wake_interval)
                events = selector.select(timeout=timeout)

                finished_builds.clear()

                # The transition "suspended to foreground/background" is handled in the signal
                # handler, but there's no SIGCONT event in the transition of background to
                # foreground, so the terminal polls for that here (headless case, where the wake
                # interval above bounds the poll rate).
                if terminal is not None:
                    terminal.poll_foreground()

                for key, _ in events:
                    data = key.data
                    if isinstance(data, FdInfo):
                        # Child output (logs and state updates)
                        child_info = self.running_builds[data.build_id]
                        if data.name == "output":
                            self._handle_child_logs(child_info, selector)
                        elif data.name == "state":
                            self._handle_child_state(child_info, selector)
                        elif data.name == "sentinel":
                            finished_builds.append(data.build_id)
                    elif data == STDIN_EVENT:
                        stdin_ready = True
                    elif data == SIGWINCH_EVENT:
                        assert terminal is not None
                        terminal.drain_sigwinch()
                        self.ui.on_resize()
                    elif data == JOBSERVER_EVENT and not jobserver.has_target_parallelism():
                        jobserver.maybe_discard_tokens()
                        self.ui.on_jobs_changed(jobserver.num_jobs, jobserver.target_jobs)

                current_time = time.monotonic()
                for build_id in finished_builds:
                    self._handle_finished_build(
                        build_id, current_time, jobserver, selector, failures, database_actions
                    )

                if failures and self.fail_fast:
                    # Terminate other builds to actually fail fast. We continue in the event loop
                    # waiting for child processes to finish, which may take a little while.
                    for child in self.running_builds.values():
                        child.proc.terminate()
                    self.pending_builds.clear()
                    self.pending_expansions.clear()

                if stdin_ready and terminal is not None:
                    self.ui.on_input(terminal.read_input())

                # Try to expand build deps for cache-miss specs. This requires a read lock on the
                # database, meaning that it can take several iterations of the event loop in case
                # of contention with other processes.
                if self.pending_expansions:
                    self._try_expand_build_deps()

                # Try to schedule more builds, acquiring per-spec locks and jobserver tokens.
                if self.capacity and self.pending_builds:
                    blocked = self._schedule_builds(
                        selector, jobserver, retained_read_locks, database_actions
                    )

                # Flush finished builds to the database if a write is due. This runs after
                # scheduling so that a final mark-explicit action does not wait for the next
                # select() timeout.
                self._flush_db_if_due(current_time, database_actions, retained_read_locks)

                # Execute commands produced by the UI ahead of rendering.
                self._run_ui_commands(jobserver)

                # Finally update the UI
                self.ui.render()
        finally:
            # Restore input settings and signal handlers. On POSIX this runs TCSADRAIN,
            # ensuring buffered cursor-movement codes from the event loop are transmitted
            # before the final render.
            if terminal is not None:
                terminal.teardown_input()

            # Flush any not-yet-written successful builds to the DB; save the exception on error
            # to be re-raised after best-effort cleanup.
            db_exc = None
            if database_actions:
                try:
                    db = self.store.db
                    with db.write_transaction():
                        for action in database_actions:
                            action.save_to_db(db)
                except Exception as e:
                    db_exc = e

            # Send SIGTERM to running builds; this is a no-op in the successful case.
            for child in self.running_builds.values():
                try:
                    child.proc.terminate()
                except Exception:
                    pass

            # Release our jobserver token for each terminated build and then join.
            for child in self.running_builds.values():
                try:
                    jobserver.release()
                    child.proc.join(timeout=30)
                    if child.proc.is_alive():
                        child.proc.kill()
                        child.proc.join()
                except Exception:
                    pass

            # Release all held locks best-effort, so that one failure does not prevent the others
            # from being released.
            for child in self.running_builds.values():
                child.release_prefix_lock()

            for lock in retained_read_locks:
                try:
                    lock.release_read()
                except Exception:
                    pass
            for action in database_actions:
                action.release_prefix_lock()

            try:
                self.ui.render(finalize=True)
            except Exception:
                pass
            try:
                selector.close()
            except Exception:
                pass
            try:
                jobserver.close()
            except Exception:
                pass

            # Restore output settings. On Linux this is a no-op. On Windows this disables
            # VT100 processing and must happen after the final render.
            if terminal is not None:
                terminal.teardown_output()

            # Re-raise the DB exception if any.
            if db_exc is not None:
                raise db_exc

        try:
            self.report_data.finalize(self.reports, build_graph=self.build_graph)
        except Exception as e:
            spack.util.tty.debug(f"[{__name__}]: Failed to finalize reports: {e}")

        # Clean up temp log files of successful builds now that reports have consumed them.
        if not self.keep_stage:
            failed_hashes = {s.dag_hash() for s in failures}
            for dag_hash, log_path in self.log_paths.items():
                if log_path == os.devnull or dag_hash in failed_hashes:
                    continue
                try:
                    os.unlink(log_path)
                except OSError:
                    pass

        self.ui.on_finished([s.dag_hash() for s in failures])

        if failures:
            lines = [f"{s}: {self.log_paths[s.dag_hash()]}" for s in failures]
            raise spack.error.InstallError(
                "The following packages failed to install:\n" + "\n".join(lines)
            )

    def _handle_finished_build(
        self,
        dag_hash: str,
        current_time: float,
        jobserver: JobServerBase,
        selector: selectors.BaseSelector,
        failures: List[spack.spec.Spec],
        database_actions: List[DatabaseAction],
    ) -> None:
        """Handle a build that has finished. Remove from running_builds; release jobserver token;
        update UI state; defer database insertion if successful; possibly reschedule if failed with
        cache miss; register failures."""
        build = self.running_builds.pop(dag_hash)
        self.capacity += 1
        jobserver.release()
        self.ui.on_jobs_changed(jobserver.num_jobs, jobserver.target_jobs)
        self._drain_child_output(build, selector)
        self._drain_child_state(build, selector)
        exitcode = build.close(selector)
        self.report_data.finish_record(build.spec, exitcode, build.log_path)

        if exitcode == ExitCode.SUCCESS:
            # Schedule successful builds for batched database insertion. Ownership of the prefix
            # write lock moves from the finished child to the pending DB insert; it is downgraded
            # or released only after a successful db write.
            database_actions.append(
                AddSpecAction(build.spec, dag_hash in self.explicit, build.prefix_lock)
            )
            build.prefix_lock = None
            self.build_graph.enqueue_parents(dag_hash, self.pending_builds)
            self.next_database_write = current_time + DATABASE_WRITE_INTERVAL
            self.ui.on_state_changed(dag_hash, "finished")
            return

        # When we don't have to do a db write, we can release the lock immediately.
        build.release_prefix_lock()

        is_root = dag_hash in self.build_graph.roots
        user_policy = self.root_policy if is_root else self.dependencies_policy

        if exitcode == ExitCode.STOPPED_AT_PHASE:
            return  # the user requested early stopping; don't treat as failure
        elif exitcode == ExitCode.BUILD_CACHE_MISS and user_policy == "auto":
            # Check if we can reschedule this as a source build after a build cache miss. If so,
            # return early without recording a failure.
            self.build_graph.force_source.add(dag_hash)
            self.ui.on_build_removed(dag_hash)
            if self.build_graph.has_unexpanded_build_deps(dag_hash):
                self.pending_expansions.append(dag_hash)
            else:
                self.pending_builds.append(dag_hash)
        elif not failures or not self.fail_fast:
            # Record a failure. In fail-fast mode, only record the first failure; subsequent
            # failures may be a consequence of us terminating other builds.
            failures.append(build.spec)
            self.ui.on_state_changed(dag_hash, "failed")

    def _try_expand_build_deps(self) -> None:
        """Try to expand build deps for specs with cache misses. Non-blocking: returns immediately
        if the DB read lock is unavailable."""
        db = self.store.db
        with db.try_read_transaction() as acquired:
            if not acquired:
                return
            dep_policy = (
                "source_only"
                if (self.dependencies_policy == "auto" and not self.has_mirrors)
                else self.dependencies_policy
            )
            newly_added = self.build_graph.expand_build_deps(
                self.pending_expansions, self.pending_builds, db, dep_policy
            )
            for h in newly_added:
                self.binary_cache_for_spec[h] = (
                    spack.binary_distribution.BINARY_INDEX.find_by_hash(h)
                )
            self.ui.on_total_increased(len(newly_added))
            self.pending_expansions.clear()

    def _flush_db_if_due(
        self,
        current_time: float,
        database_actions: List[DatabaseAction],
        retained_read_locks: List[spack.util.lock.Lock],
    ) -> None:
        """Write finished builds to the database if the write interval has passed, or if all
        builds are done. The write is not guaranteed; it fails if another process holds the lock,
        in which case it is retried in a later iteration of the event loop."""
        if (
            database_actions
            and (
                current_time >= self.next_database_write
                or not (self.pending_builds or self.running_builds)
            )
            and self._save_to_db(database_actions, retained_read_locks)
        ):
            database_actions.clear()

    def _save_to_db(
        self,
        database_actions: List[DatabaseAction],
        retained_read_locks: List[spack.util.lock.Lock],
    ) -> bool:
        db = self.store.db
        with db.try_write_transaction() as acquired:
            if not acquired:
                return False
            for action in database_actions:
                action.save_to_db(db)

        # DB has been written and flushed; downgrade per-spec prefix write locks to read locks so
        # other processes can see the specs are installed, while preventing concurrent uninstalls.
        for action in database_actions:
            if action.prefix_lock is not None:
                try:
                    action.prefix_lock.downgrade_write_to_read()
                    retained_read_locks.append(action.prefix_lock)
                except Exception:
                    action.prefix_lock.release_write()
                    raise
                finally:
                    action.prefix_lock = None

        return True

    def _schedule_builds(
        self,
        selector: selectors.BaseSelector,
        jobserver: JobServerBase,
        retained_read_locks: List[spack.util.lock.Lock],
        database_actions: List[DatabaseAction],
    ) -> bool:
        """Try to schedule as many pending builds as possible.

        Delegates to the module-level schedule_builds() function and then performs the
        side-effects that require the selector and running-build state: updating the UI for
        specs that were found already installed, updating the UI's blocked indicator, and
        launching new builds via _start().

        Preconditions: self.capacity > 0 and self.pending_builds is not empty.

        Returns True if we had capacity to schedule, but were blocked by locks held by other
        processes. In that case we should not monitor the jobserver for new tokens, since we'd end
        up in a busy wait loop until the locks are released.
        """
        result = schedule_builds(
            pending=self.pending_builds,
            build_graph=self.build_graph,
            store=self.store,
            overwrite=self.overwrite,
            overwrite_time=self.overwrite_time,
            capacity=self.capacity,
            needs_jobserver_token=bool(self.running_builds),
            jobserver=jobserver,
            explicit=self.explicit,
        )
        blocked = result.blocked
        database_actions.extend(result.to_mark_explicit)
        # Specs installed by another process.
        for dag_hash, spec, lock in result.newly_installed:
            retained_read_locks.append(lock)
            self.ui.on_build_added(self._build_info(spec, explicit=dag_hash in self.explicit))
            self.ui.on_state_changed(dag_hash, "finished")
        # Specs we can start building ourselves.
        for dag_hash, lock in result.to_start:
            self._start(selector, jobserver, dag_hash, lock)
        self.ui.on_blocked_changed(blocked and not self.running_builds)
        return blocked

    def _effective_install_policy(self, dag_hash: str, is_root: bool) -> InstallPolicy:
        """Compute the effective install policy based on the user policy and dynamic factors such
        as build cache availability and whether build dependencies can be skipped."""
        if dag_hash in self.build_graph.force_source:
            return "source_only"
        policy = self.root_policy if is_root else self.dependencies_policy
        if policy == "auto" and not self.has_mirrors:
            return "source_only"
        if policy == "auto" and not self.include_build_deps:
            # In case we don't require build deps and we have a binary cache configured, we install
            # build dependencies only if needed. This works in two steps: force a cache_only
            # install, and if that fails, add to force_source and schedule build deps so that a
            # second attempt uses the source_only policy. Therefore, return cache_only here.
            return "cache_only"
        return policy

    def _start(
        self,
        selector: selectors.BaseSelector,
        jobserver: JobServerBase,
        dag_hash: str,
        prefix_lock: spack.util.lock.Lock,
    ) -> None:
        self.capacity -= 1
        explicit = dag_hash in self.explicit
        spec = self.build_graph.nodes[dag_hash]
        is_develop = spec.is_develop
        tests = self.tests
        run_tests = tests is True or bool(tests and spec.name in tests)
        is_root = dag_hash in self.build_graph.roots
        # Both possible sub-processes (cache install, source build) append to the same log file.
        if dag_hash not in self.log_paths:
            if spec.external:
                self.log_paths[dag_hash] = os.devnull
            else:
                prefix = fs.polite_filename(
                    f"spack-stage-{spec.name}-{spec.version}-{spec.dag_hash()}-"
                )
                log_fd, log_path = tempfile.mkstemp(
                    prefix=prefix, suffix=".log", dir=spack.stage.get_stage_root()
                )
                os.close(log_fd)
                self.log_paths[dag_hash] = log_path

        request = BuildRequest(
            spec=spec,
            explicit=explicit,
            mirrors=self.binary_cache_for_spec[dag_hash],
            unsigned=self.unsigned,
            install_policy=self._effective_install_policy(dag_hash, is_root),
            dirty=self.dirty,
            # keep_stage/restage logic taken from installer.py
            keep_stage=self.keep_stage or is_develop,
            restage=self.restage and not is_develop,
            keep_prefix=self.keep_prefix,
            skip_patch=self.skip_patch,
            fake=self.fake,
            install_source=self.install_source,
            run_tests=run_tests,
            log_path=self.log_paths[dag_hash],
            stop_before=self.stop_before if is_root else None,
            stop_at=self.stop_at if is_root else None,
        )
        child_info = self.launcher(request, jobserver)
        child_info.prefix_lock = prefix_lock
        self.running_builds[dag_hash] = child_info
        child_info.register_with_selector(selector, dag_hash)
        self.ui.on_build_added(
            self._build_info(child_info.spec, explicit=explicit, log_path=child_info.log_path)
        )
        self.report_data.start_record(spec)

    def _build_info(
        self, spec: spack.spec.Spec, explicit: bool, log_path: Optional[str] = None
    ) -> BuildInfo:
        """Create the UI payload for a build: plain data extracted from the spec."""
        return BuildInfo(
            spec.dag_hash(),
            name=spec.name,
            version=str(spec.version),
            external=spec.external,
            prefix=spec.prefix,
            explicit=explicit,
            log_path=log_path,
        )

    def _run_ui_commands(self, jobserver: JobServerBase) -> None:
        """Execute the commands produced by the UI."""
        if not self.ui.commands:
            return
        commands, self.ui.commands = self.ui.commands, []
        for cmd in commands:
            if isinstance(cmd, SetEcho):
                self._set_echo(cmd.build_id, cmd.echo)
            else:  # ChangeJobs
                if cmd.delta > 0:
                    jobserver.increase_parallelism()
                else:
                    jobserver.decrease_parallelism()
                self.ui.on_jobs_changed(jobserver.num_jobs, jobserver.target_jobs)

    def _set_echo(self, build_id: str, echo: bool) -> None:
        """Enable or disable log forwarding from a running build to this process."""
        child = self.running_builds.get(build_id)
        if child is None:
            return
        try:
            write_connection(child.control_w_conn, b"1" if echo else b"0")
        except OSError:
            pass

    def _handle_child_logs(self, child_info: ChildInfo, selector: selectors.BaseSelector) -> bool:
        """Handle reading output logs from a child process pipe. Returns False once the channel
        has reached EOF and was unregistered, True while it remains open."""
        conn = child_info.output_r_conn
        try:
            # There might be more data than OUTPUT_BUFFER_SIZE, but we will read that in the next
            # iteration of the event loop to keep things responsive.
            data = read_connection(conn, OUTPUT_BUFFER_SIZE)
        except BlockingIOError:
            return True
        except OSError:
            data = None

        if not data:  # EOF or error
            try:
                selector.unregister(conn)
            except (KeyError, OSError):
                pass
            return False

        self.ui.on_log_output(child_info.spec.dag_hash(), data)
        return True

    def _drain_child_output(self, child_info: ChildInfo, selector: selectors.BaseSelector) -> None:
        """Read and print any remaining output from a finished child's pipe."""
        while self._handle_child_logs(child_info, selector):
            pass

    def _drain_child_state(self, child_info: ChildInfo, selector: selectors.BaseSelector) -> None:
        """Read and process any remaining state messages from a finished child's pipe."""
        # Must drain before child.close() to consume any remaining data before bridges close.
        while self._handle_child_state(child_info, selector):
            pass

    def _handle_child_state(self, child_info: ChildInfo, selector: selectors.BaseSelector) -> bool:
        """Handle reading state updates from a child process pipe. Returns False once the channel
        has reached EOF and was unregistered, True while it remains open."""
        conn = child_info.state_r_conn
        dag_hash = child_info.spec.dag_hash()
        try:
            # There might be more data than OUTPUT_BUFFER_SIZE, but we will read that in the next
            # iteration of the event loop to keep things responsive.
            data = read_connection(conn, OUTPUT_BUFFER_SIZE)
        except BlockingIOError:
            return True
        except OSError:
            data = None

        if not data:  # EOF or error
            try:
                selector.unregister(conn)
            except (KeyError, OSError):
                pass
            child_info.state_buffer = b""
            return False

        # Accumulate raw bytes and split on the newline byte. We never decode a partial read; only
        # complete lines are handed to json.loads(), which decodes the (UTF-8) bytes itself.
        buffer = child_info.state_buffer + data
        lines = buffer.split(b"\n")
        # The last element of split() will be a partial line or an empty string.
        # We store it back in the buffer for the next read.
        child_info.state_buffer = lines.pop()

        for line in lines:
            if not line:
                continue
            try:
                message = json.loads(line)
            except ValueError:
                continue
            if "state" in message:
                self.ui.on_state_changed(dag_hash, message["state"])
            elif "progress" in message and "total" in message:
                self.ui.on_progress(dag_hash, message["progress"], message["total"])
            elif "installed_from_binary_cache" in message:
                child_info.spec.package.installed_from_binary_cache = True

        return True
