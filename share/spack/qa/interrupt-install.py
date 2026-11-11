#!/usr/bin/env python3
# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Press Ctrl-C in a terminal that runs ``spack install``, and check that Spack stops the build,
that the build cleans up after itself, and that Spack exits by SIGINT.

Unlike the unit tests, this delivers Ctrl-C the way a terminal does: to the foreground process
group of a pty on POSIX, and to every process attached to the console on Windows. It installs the
``blocking-install`` package from the mock repository, into a temporary directory."""

import glob
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time

SPACK_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
MOCK_REPO = os.path.join(SPACK_ROOT, "var", "spack", "test_repos", "spack_repo", "builtin_mock")
TIMEOUT = 120.0

CONFIG_YAML = """\
config:
  install_tree:
    root: '{0}/opt'
  build_stage: ['{0}/stage']
"""

REPOS_YAML = """\
repos::
  builtin_mock: '{0}'
"""

#: Without these entries Spack looks for the Windows SDK when it concretizes on Windows
PACKAGES_YAML = """\
packages:
  win-sdk:
    buildable: false
  wgl:
    buildable: false
"""


class Sandbox:
    """A temporary install tree and the configuration scope that points Spack at it."""

    def __init__(self) -> None:
        self.root = tempfile.mkdtemp(prefix="spack-interrupt-").replace("\\", "/")
        for name, content in (
            ("config.yaml", CONFIG_YAML.format(self.root)),
            ("repos.yaml", REPOS_YAML.format(MOCK_REPO.replace("\\", "/"))),
            ("packages.yaml", PACKAGES_YAML),
        ):
            with open(os.path.join(self.root, name), "w", encoding="utf-8") as f:
                f.write(content)

    def install_command(self) -> list:
        spack = os.path.join(SPACK_ROOT, "bin", "spack")
        return [sys.executable, spack, "-C", self.root, "install", "blocking-install"]

    def prefix(self, name: str = "") -> str:
        """Path of the prefix of the build, or of a file in it; empty if it does not exist."""
        pattern = os.path.join(self.root, "opt", "**", "blocking-install-*", name)
        return next(iter(glob.glob(pattern, recursive=True)), "")


def interrupt_in_pty(sandbox: Sandbox) -> "tuple[bool, str]":
    """Run the install in a pty, and press Ctrl-C once the build blocks. Returns whether Spack
    exited by SIGINT, and the terminal output."""
    import pty
    import select

    pid, fd = pty.fork()
    if pid == 0:
        command = sandbox.install_command()
        os.execv(command[0], command)

    output = b""
    pressed = False
    deadline = time.monotonic() + TIMEOUT
    while True:
        if select.select([fd], [], [], 0.05)[0]:
            try:
                output += os.read(fd, 65536)
            except OSError:
                pass
        if not pressed and sandbox.prefix("ready"):
            os.write(fd, b"\x03")
            pressed = True
        done, status = os.waitpid(pid, os.WNOHANG)
        if done:
            by_sigint = os.WIFSIGNALED(status) and os.WTERMSIG(status) == signal.SIGINT
            return by_sigint, output.decode("utf-8", "replace")
        if time.monotonic() > deadline:
            os.kill(pid, signal.SIGKILL)
            sys.exit("spack install did not exit:\n" + output.decode("utf-8", "replace"))


def send_ctrl_c(pid: int) -> None:
    """Send Ctrl-C to the console of the given process. This runs in a process of its own, since
    it has to leave its console for that."""
    import ctypes

    kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
    kernel32.FreeConsole()
    if not kernel32.AttachConsole(pid):
        sys.exit("cannot attach to the console of process {0}".format(pid))
    kernel32.SetConsoleCtrlHandler(None, True)  # ignore the Ctrl-C ourselves
    kernel32.GenerateConsoleCtrlEvent(0, 0)
    time.sleep(1)  # stay attached until the event is delivered


def interrupt_in_console(sandbox: Sandbox) -> "tuple[bool, str]":
    """Run the install in a new console, and press Ctrl-C once the build blocks. Returns whether
    Spack exited with the code for SIGINT, and its output, which goes to a file since the console
    is not ours to read."""
    import ctypes

    # Processes inherit whether they ignore Ctrl-C, which CI runners may do
    ctypes.windll.kernel32.SetConsoleCtrlHandler(None, False)  # type: ignore[attr-defined]
    new_console = 0x00000010
    log = os.path.join(sandbox.root, "output.txt")
    with open(log, "wb") as f:
        proc = subprocess.Popen(
            sandbox.install_command(),
            stdin=subprocess.DEVNULL,
            stdout=f,
            stderr=subprocess.STDOUT,
            creationflags=new_console,
        )

    def output() -> str:
        with open(log, "rb") as f:
            return f.read().decode("utf-8", "replace")

    deadline = time.monotonic() + TIMEOUT
    while not sandbox.prefix("ready"):
        if proc.poll() is not None or time.monotonic() > deadline:
            proc.kill()
            proc.wait()
            sys.exit("the build did not start:\n" + output())
        time.sleep(0.05)
    script = os.path.abspath(__file__)
    subprocess.check_call([sys.executable, script, "--send-ctrl-c", str(proc.pid)])
    try:
        # Windows has no signals to exit by: the exit code is the signal number
        return proc.wait(TIMEOUT) == signal.SIGINT, output()
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        sys.exit("spack install did not exit:\n" + output())


def main() -> int:
    if sys.argv[1:2] == ["--send-ctrl-c"]:
        send_ctrl_c(int(sys.argv[2]))
        return 0

    sandbox = Sandbox()
    try:
        interrupt = interrupt_in_console if sys.platform == "win32" else interrupt_in_pty
        by_sigint, output = interrupt(sandbox)
        failures = []
        if not by_sigint:
            failures.append("spack did not exit by SIGINT")
        if sandbox.prefix():
            failures.append("the build did not remove its prefix")
        for failure in failures:
            print("FAILED: " + failure)
        if failures:
            print(output)
        return 1 if failures else 0
    finally:
        shutil.rmtree(sandbox.root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
