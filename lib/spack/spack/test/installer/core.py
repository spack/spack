# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for the installer.core module: the PackageInstaller event loop."""

import os
import selectors
import signal
import sys
import time

import pytest

import spack.concretize
import spack.error
import spack.spec
from spack.config import Configuration
from spack.installer.base import STOP_SIGNALS, ExitCode
from spack.installer.core import PackageInstaller, SignalEvents, read_connection, write_connection
from spack.installer.ui import ChangeJobs, SetEcho
from spack.store import Store
from spack.test.installer.conftest import (
    DrivingUI,
    RecordingUI,
    Script,
    ScriptedLauncher,
    _install,
    _make_concrete,
    _record,
)


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

    def test_older_readable_db_fails_before_building(self, mutable_database, bumped_db_version):
        """Nothing is built when the database needs an explicit reindex to be modified, but
        an installer with nothing to do does not complain."""
        installed = mutable_database.query_local("libelf")[0]
        PackageInstaller([installed.package])

        spec = spack.spec.Spec("trivial-install-test-package")
        spec._mark_concrete()
        with pytest.raises(spack.error.ExplicitDatabaseUpgradeError):
            PackageInstaller([spec.package])


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


@pytest.mark.disable_clean_stage_check
def test_build_exiting_without_exit_code_fails(temporary_store, mock_packages):
    """Only the exit code reported by the build counts: a build that exits without one failed."""
    spec = _make_concrete("trivial-install-test-package")
    launcher = ScriptedLauncher({spec.name: Script(exitcode=None)})
    with pytest.raises(spack.error.InstallError):
        _install(launcher, spec)
    assert _record(temporary_store, spec) is None


def test_cache_miss_falls_back_to_source_build(
    temporary_store: Store, mock_packages, mutable_config: Configuration, tmp_path
):
    """With a binary mirror configured, the first attempt is cache_only; a cache miss removes the
    build from the UI, reschedules it as source_only, and the second attempt succeeds."""
    mutable_config.set(
        "mirrors", {"local": {"url": (tmp_path / "mirror").as_uri(), "binary": True}}
    )
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


@pytest.mark.disable_clean_stage_check  # failed builds keep their log file in the stage root
def test_builds_that_do_not_terminate_are_killed(temporary_store, mock_packages):
    """A build that is still running when the terminate timeout expires is killed."""
    bad, hanging = _make_concrete("pkg-a"), _make_concrete("pkg-b")
    launcher = ScriptedLauncher(
        {
            bad.name: Script(exitcode=ExitCode.BUILD_ERROR),
            hanging.name: Script(hang=True, ignore_terminate=True),
        }
    )
    with pytest.raises(spack.error.InstallError):
        _install(
            launcher, bad, hanging, fail_fast=True, concurrent_packages=2, terminate_timeout=0.0
        )

    assert launcher.hanging[0].terminated and launcher.hanging[0].killed


def test_set_echo_commands_reach_control_channel(temporary_store, mock_packages):
    """SetEcho commands queued by the UI are written as b"1"/b"0" to the control channel of the
    build, which is still registered as running when the command queue is drained."""
    spec = _make_concrete("trivial-install-test-package")
    launcher = ScriptedLauncher({spec.name: Script()})
    ui = RecordingUI()
    ui.commands += [SetEcho(spec.dag_hash(), True), SetEcho(spec.dag_hash(), False)]
    _install(launcher, spec, ui=ui)

    assert read_connection(launcher.builds[0].channels.control_r, 16) == b"10"


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


def _skip_if_handled_by_test_runner():
    if len(SignalEvents(STOP_SIGNALS).old_handlers) < len(STOP_SIGNALS):
        pytest.skip("stop signals are handled by the test runner")


def _send(signum):
    """Send a signal to this process."""
    if sys.platform == "win32":
        # os.kill() terminates the process on Windows
        signal.raise_signal(signum)  # novermin
    else:
        os.kill(os.getpid(), signum)


def _stop_error(signum):
    """The exception that install() raises after the given signal stopped it."""
    return KeyboardInterrupt if signum == signal.SIGINT else spack.error.TerminatedBySignal


@pytest.mark.disable_clean_stage_check  # interrupted installs keep their log files
@pytest.mark.parametrize("signum", STOP_SIGNALS, ids=lambda s: s.name)
def test_stop_signal_terminates_builds(signum, temporary_store, mock_packages):
    """A stop signal terminates the running builds. The event loop ends when they have exited,
    restores the signal handlers, and raises."""
    _skip_if_handled_by_test_runner()
    spec = _make_concrete("trivial-install-test-package")
    launcher = ScriptedLauncher({spec.name: Script(hang=True)})
    handlers = [signal.getsignal(s) for s in STOP_SIGNALS]

    def tick():
        if launcher.hanging and not launcher.hanging[0].terminated:
            _send(signum)

    ui = DrivingUI(tick)
    with pytest.raises(_stop_error(signum)) as e:
        _install(launcher, spec, ui=ui)

    assert signum == signal.SIGINT or e.value.signum == signum
    assert launcher.hanging[0].terminated and not launcher.hanging[0].killed
    assert ("stopping",) in ui.events
    assert not [e for e in ui.events if e[0] == "state_changed" and e[2] == "failed"]
    assert [signal.getsignal(s) for s in STOP_SIGNALS] == handlers


@pytest.mark.disable_clean_stage_check  # interrupted installs keep their log files
@pytest.mark.parametrize("signum", STOP_SIGNALS, ids=lambda s: s.name)
def test_stop_signal_while_starting_build(signum, temporary_store, mock_packages):
    """A stop signal while a build is started terminates that build."""
    _skip_if_handled_by_test_runner()
    spec = _make_concrete("trivial-install-test-package")
    launcher = ScriptedLauncher({spec.name: Script(hang=True)})

    def launch(request, jobserver):
        child = launcher(request, jobserver)
        _send(signum)
        return child

    with pytest.raises(_stop_error(signum)):
        _install(launch, spec)

    assert launcher.hanging[0].terminated


@pytest.mark.disable_clean_stage_check  # interrupted installs keep their log files
def test_build_finishing_while_stopping(temporary_store, mock_packages):
    """A build that finishes successfully after a stop signal is added to the database, and its
    dependents are not started."""
    _skip_if_handled_by_test_runner()
    dep = _make_concrete("dependency-install")
    root = _make_concrete("dependent-install", deps=[dep])
    launcher = ScriptedLauncher({dep.name: Script(hang=True), root.name: Script()})

    def tick():
        if launcher.hanging and not launcher.hanging[0].finished:
            _send(signal.SIGINT)
            launcher.hanging[0].finish()

    with pytest.raises(KeyboardInterrupt):
        _install(launcher, root, ui=DrivingUI(tick))

    assert [r.spec.name for r in launcher.requests] == [dep.name]
    assert _record(temporary_store, dep) is not None


@pytest.mark.disable_clean_stage_check  # interrupted installs keep their log files
def test_second_interrupt_kills_builds(temporary_store, mock_packages):
    """Ctrl-C while the builds are terminating kills them, instead of waiting for the timeout."""
    _skip_if_handled_by_test_runner()
    spec = _make_concrete("trivial-install-test-package")
    launcher = ScriptedLauncher({spec.name: Script(hang=True, ignore_terminate=True)})

    def tick():
        if launcher.hanging and not launcher.hanging[0].killed:
            _send(signal.SIGINT)

    with pytest.raises(KeyboardInterrupt):
        _install(launcher, spec, ui=DrivingUI(tick))

    assert launcher.hanging[0].killed


@pytest.mark.disable_clean_stage_check  # interrupted installs keep their log files
def test_interrupt_does_not_terminate_builds_that_receive_it(temporary_store, mock_packages):
    """The event loop does not terminate a build that receives Ctrl-C too, like builds on Windows,
    where that would kill the build before it has cleaned up. It waits for the build to exit."""
    _skip_if_handled_by_test_runner()
    spec = _make_concrete("trivial-install-test-package")
    launcher = ScriptedLauncher({spec.name: Script(hang=True, receives_interrupt=True)})

    def tick():
        if ("stopping",) in ui.events:
            launcher.hanging[0].finish()
        elif launcher.hanging:
            _send(signal.SIGINT)

    ui = DrivingUI(tick)
    with pytest.raises(KeyboardInterrupt):
        _install(launcher, spec, ui=ui)

    assert not launcher.hanging[0].terminated and not launcher.hanging[0].killed


def _is_unlocked(path):
    """Whether the process that holds a lock on the file has exited. Unlike a pid, this is not
    fooled by a process that nobody reaps."""
    import fcntl

    with open(path, "rb") as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except OSError:
            return False


@pytest.mark.not_on_windows("Windows does not have process groups")
@pytest.mark.disable_clean_stage_check  # interrupted installs keep their log files
@pytest.mark.parametrize("ignore_sigterm", [False, True])
def test_interrupt_running_build(ignore_sigterm, install_mockery):
    """Ctrl-C terminates a build and its child process, and the build removes its prefix. If the
    child process ignores SIGTERM, a second Ctrl-C kills it."""
    _skip_if_handled_by_test_runner()
    variant = "+ignore_sigterm" if ignore_sigterm else "~ignore_sigterm"
    spec = spack.concretize.concretize_one(f"blocking-install {variant}")
    lock, ready = os.path.join(spec.prefix, "lock"), os.path.join(spec.prefix, "ready")
    interrupts = []

    def tick():
        if os.path.exists(ready) and len(interrupts) < (2 if ignore_sigterm else 1):
            interrupts.append(time.monotonic())
            _send(signal.SIGINT)

    installer = PackageInstaller(
        [spec.package], explicit=True, ui=DrivingUI(tick), terminate_timeout=60.0
    )
    with pytest.raises(KeyboardInterrupt):
        installer.install()

    assert time.monotonic() - interrupts[0] < 30
    if ignore_sigterm:
        # The build was killed. Its child process dies with it, perhaps slightly later.
        while not _is_unlocked(lock):
            assert time.monotonic() - interrupts[0] < 30
            time.sleep(0.01)
    else:
        assert not os.path.exists(spec.prefix)


def test_third_interrupt_raises_keyboard_interrupt():
    """The event loop handles Ctrl-C twice; after that it is raised as usual, so that an event loop
    that does not respond can still be interrupted."""
    _skip_if_handled_by_test_runner()
    signal_events = SignalEvents([signal.SIGINT])
    with selectors.DefaultSelector() as selector:
        signal_events.setup(selector)
        try:
            _send(signal.SIGINT)
            _send(signal.SIGINT)
            assert signal_events.read() == bytes([signal.SIGINT, signal.SIGINT])
            with pytest.raises(KeyboardInterrupt):
                _send(signal.SIGINT)
                time.sleep(1)  # the handler runs between two bytecodes
        finally:
            assert signal_events.teardown(STOP_SIGNALS) == signal.SIGINT
    assert signal.getsignal(signal.SIGINT) is signal.default_int_handler


@pytest.mark.not_on_windows("Windows has no termination signals to handle")
@pytest.mark.disable_clean_stage_check  # interrupted installs keep their log files
def test_termination_signal_during_cleanup(temporary_store, mock_packages):
    """A termination signal during the cleanup after another exception does not interrupt the
    cleanup, and is raised after it."""
    _skip_if_handled_by_test_runner()
    dep = _make_concrete("dependency-install")
    root = _make_concrete("dependent-install", deps=[dep])
    launcher = ScriptedLauncher({dep.name: Script(), root.name: Script(hang=True)})

    def tick():
        if launcher.hanging:
            build = launcher.hanging[0]
            terminate = build.terminate

            def signal_and_terminate():
                _send(signal.SIGTERM)
                terminate()

            build.terminate = signal_and_terminate
            raise KeyboardInterrupt

    with pytest.raises(spack.error.TerminatedBySignal) as e:
        _install(launcher, root, ui=DrivingUI(tick))

    assert isinstance(e.value.__context__, KeyboardInterrupt)
    assert launcher.hanging[0].terminated
    assert _record(temporary_store, dep) is not None
    assert signal.getsignal(signal.SIGTERM) is signal.SIG_DFL


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


@pytest.mark.disable_clean_stage_check  # interrupted and failed installs keep their log files
@pytest.mark.parametrize(
    "root_script,expected_error",
    [
        (Script(), None),
        (Script(hang=True), KeyboardInterrupt),
        (Script(exitcode=ExitCode.BUILD_ERROR), spack.error.InstallError),
    ],
)
def test_recorded_specs(root_script, expected_error, temporary_store, mock_packages):
    """Tests that the installer lists the specs it added to the database, also when the
    installation is interrupted or a build fails.
    """
    dep = _make_concrete("dependency-install")
    root = _make_concrete("dependent-install", deps=[dep])
    launcher = ScriptedLauncher({dep.name: Script(), root.name: root_script})

    def tick():
        if launcher.hanging:  # the dep finished and the root build is now running
            raise KeyboardInterrupt

    installer = PackageInstaller(
        [root.package], explicit=True, ui=DrivingUI(tick), launcher=launcher
    )
    if expected_error is None:
        installer.install()
    else:
        with pytest.raises(expected_error):
            installer.install()

    expected = [dep.dag_hash()] if expected_error else [dep.dag_hash(), root.dag_hash()]
    assert [s.dag_hash() for s in installer.recorded_specs] == expected
    assert [s.dag_hash() for s in (dep, root) if _record(temporary_store, s)] == expected
