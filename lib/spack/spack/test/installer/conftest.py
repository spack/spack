# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Shared fakes and helpers for the installer unit tests."""

import json
import signal
import socket
from typing import Callable, Dict, List, NamedTuple, Optional, Sequence, Tuple, Union

import spack.deptypes as dt
import spack.spec
from spack.installer.base import BuildChannels, ExitCode, JobServerBase, ProcessExitNotifier
from spack.installer.build import BuildRequest, ChildInfo, create_build_channels
from spack.installer.core import PackageInstaller, write_connection
from spack.installer.ui import InstallerUI
from spack.spec import Spec


def create_dag(
    nodes: List[str], edges: List[Tuple[str, str, Union[dt.DepType, Tuple[dt.DepType, ...]]]]
) -> Dict[str, Spec]:
    """
    Create a DAG of concrete specs, as a mapping from package name to Spec.

    Arguments:
        nodes: list of unique package names
        edges: list of tuples (parent, child, deptype)
    """
    specs = {name: Spec(name) for name in nodes}
    for parent, child, deptypes in edges:
        depflag = deptypes if isinstance(deptypes, dt.DepFlag) else dt.canonicalize(deptypes)
        specs[parent].add_dependency_edge(specs[child], depflag=depflag, virtuals=())

    # Mark all specs as concrete
    for spec in specs.values():
        spec._mark_concrete()

    return specs


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
