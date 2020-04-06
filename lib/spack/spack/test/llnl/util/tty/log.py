# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function
import contextlib
import os
import re
import signal
import time

try:
    import termios
except ImportError:
    termios = None

import pytest

import llnl.util.tty.log
from llnl.util.tty.log import log_output
from llnl.util.tty.pty import PseudoShell

from spack.util.executable import which


def test_log_python_output_with_python_stream(capsys, tmpdir):
    # pytest's DontReadFromInput object does not like what we do here, so
    # disable capsys or things hang.
    with tmpdir.as_cwd():
        with capsys.disabled():
            with log_output('foo.txt'):
                print('logged')

        with open('foo.txt') as f:
            assert f.read() == 'logged\n'

        assert capsys.readouterr() == ('', '')


def test_log_python_output_with_fd_stream(capfd, tmpdir):
    with tmpdir.as_cwd():
        with log_output('foo.txt'):
            print('logged')

        with open('foo.txt') as f:
            assert f.read() == 'logged\n'

        # Coverage is cluttering stderr during tests
        assert capfd.readouterr()[0] == ''


def test_log_python_output_and_echo_output(capfd, tmpdir):
    with tmpdir.as_cwd():
        with log_output('foo.txt') as logger:
            with logger.force_echo():
                print('echo')
            print('logged')

        # Coverage is cluttering stderr during tests
        assert capfd.readouterr()[0] == 'echo\n'

        with open('foo.txt') as f:
            assert f.read() == 'echo\nlogged\n'


@pytest.mark.skipif(not which('echo'), reason="needs echo command")
def test_log_subproc_output(capsys, tmpdir):
    echo = which('echo')

    # pytest seems to interfere here, so we need to use capsys.disabled()
    # TODO: figure out why this is and whether it means we're doing
    # sometihng wrong with OUR redirects.  Seems like it should work even
    # with capsys enabled.
    with tmpdir.as_cwd():
        with capsys.disabled():
            with log_output('foo.txt'):
                echo('logged')

        with open('foo.txt') as f:
            assert f.read() == 'logged\n'


@pytest.mark.skipif(not which('echo'), reason="needs echo command")
def test_log_subproc_and_echo_output(capfd, tmpdir):
    echo = which('echo')

    with tmpdir.as_cwd():
        with log_output('foo.txt') as logger:
            with logger.force_echo():
                echo('echo')
            print('logged')

        # Coverage is cluttering stderr during tests
        assert capfd.readouterr()[0] == 'echo\n'

        with open('foo.txt') as f:
            assert f.read() == 'logged\n'


#
# Tests below use a pseudoterminal to test llnl.util.tty.log
#

def mock_logger(attrs):
    """Mock logger (child) process for testing log.keyboard_input."""
    def handler(signum, frame):
        running[0] = False
    signal.signal(signal.SIGUSR1, handler)

    running = [True]
    i = 1
    with log_output("log.txt") as logger:
        with logger.force_echo():
            print(0)

        while running[0]:
            print(i)
            i += 1
            time.sleep(1e-3)

    # report final count of printed numbers
    attrs["count"] = i


def mock_shell_fg(proc, ctl, attrs):
    """Child function for test_foreground_background_* below."""
    ctl.fg()
    ctl.status()
    ctl.wait_enabled()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_fg_no_termios(proc, ctl, attrs):
    """Child function for test_foreground_background_* below."""
    ctl.fg()
    ctl.status()
    ctl.wait_disabled_fg()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_bg(proc, ctl, attrs):
    """Child function for test_foreground_background_* below."""
    ctl.bg()
    ctl.status()
    ctl.wait_disabled()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_tstp_cont(proc, ctl, attrs):
    """Child function for test_foreground_background_* below."""
    ctl.tstp()
    ctl.wait_stopped()

    ctl.cont()
    ctl.wait_running()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_tstp_tstp_cont(proc, ctl, attrs):
    """Child function for test_foreground_background_* below."""
    ctl.tstp()
    ctl.wait_stopped()

    ctl.tstp()
    ctl.wait_stopped()

    ctl.cont()
    ctl.wait_running()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_tstp_tstp_cont_cont(proc, ctl, attrs):
    """Child function for test_foreground_background_* below."""
    ctl.tstp()
    ctl.wait_stopped()

    ctl.tstp()
    ctl.wait_stopped()

    ctl.cont()
    ctl.wait_running()

    ctl.cont()
    ctl.wait_running()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_bg_fg(proc, ctl, attrs):
    """Child function for test_foreground_background_* below."""
    ctl.bg()
    ctl.status()
    ctl.wait_disabled()

    ctl.fg()
    ctl.status()
    ctl.wait_enabled()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_bg_fg_no_termios(proc, ctl, attrs):
    """Child function for test_foreground_background_* below."""
    ctl.bg()
    ctl.status()
    ctl.wait_disabled()

    ctl.fg()
    ctl.status()
    ctl.wait_disabled_fg()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_fg_bg(proc, ctl, attrs):
    """Child function for test_foreground_background_* below."""
    ctl.fg()
    ctl.status()
    ctl.wait_enabled()

    ctl.bg()
    ctl.status()
    ctl.wait_disabled()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_fg_bg_no_termios(proc, ctl, attrs):
    """Child function for test_foreground_background_* below."""
    ctl.fg()
    ctl.status()
    ctl.wait_disabled_fg()

    ctl.bg()
    ctl.status()
    ctl.wait_disabled()

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_v_v(proc, ctl, attrs):
    """Child function for test_foreground_background_* below."""
    ctl.fg()
    ctl.wait_enabled()

    time.sleep(.1)
    ctl.write(b'v')
    time.sleep(.1)
    ctl.write(b'v')
    time.sleep(.1)

    os.kill(proc.pid, signal.SIGUSR1)


def mock_shell_v_v_no_termios(proc, ctl, attrs):
    """Child function for test_foreground_background_* below."""
    ctl.fg()
    ctl.wait_disabled_fg()

    time.sleep(.1)  # allow some time to NOT print
    ctl.write(b'v\n')
    time.sleep(.1)  # allow some time to print
    ctl.write(b'v\n')
    time.sleep(.1)

    os.kill(proc.pid, signal.SIGUSR1)


@contextlib.contextmanager
def no_termios():
    saved = llnl.util.tty.log.termios
    llnl.util.tty.log.termios = None
    try:
        yield
    finally:
        llnl.util.tty.log.termios = saved


@contextlib.contextmanager
def nullcontext():
    yield


@pytest.mark.skipif(not which("ps"), reason="requires ps utility")
@pytest.mark.skipif(not termios, reason="requires termios support")
@pytest.mark.parametrize('test_fn,termios_on_or_off', [
    # tests with termios
    (mock_shell_fg, nullcontext),
    (mock_shell_bg, nullcontext),
    (mock_shell_bg_fg, nullcontext),
    (mock_shell_fg_bg, nullcontext),
    (mock_shell_tstp_cont, nullcontext),
    (mock_shell_tstp_tstp_cont, nullcontext),
    (mock_shell_tstp_tstp_cont_cont, nullcontext),
    # tests without termios
    (mock_shell_fg_no_termios, no_termios),
    (mock_shell_bg, no_termios),
    (mock_shell_bg_fg_no_termios, no_termios),
    (mock_shell_fg_bg_no_termios, no_termios),
    (mock_shell_tstp_cont, no_termios),
    (mock_shell_tstp_tstp_cont, no_termios),
    (mock_shell_tstp_tstp_cont_cont, no_termios),
])
def test_foreground_background(test_fn, termios_on_or_off):
    """Functional tests for foregrounding and backgrounding a logged process.

    This ensures that things like SIGTTOU are not raised and that
    terminal settings are corrected on foreground/background and on
    process stop and start.

    """
    shell = PseudoShell(test_fn, mock_logger)
    shell.attrs["debug"] = True

    # run the shell test
    with termios_on_or_off():
        shell.start()
    exitcode = shell.join()

    # processes completed successfully
    assert exitcode == 0


@pytest.mark.skipif(not which("ps"), reason="requires ps utility")
@pytest.mark.skipif(not termios, reason="requires termios support")
@pytest.mark.parametrize('test_fn,termios_on_or_off', [
    (mock_shell_v_v, nullcontext),
    (mock_shell_v_v_no_termios, no_termios),
])
def test_foreground_background_output(test_fn, capfd, termios_on_or_off):
    """Tests hitting 'v' toggles output, and that force_echo works."""
    shell = PseudoShell(test_fn, mock_logger)
    shell.attrs["debug"] = True

    with termios_on_or_off():
        shell.start()
    exitcode = shell.join()

    out, err = capfd.readouterr()

    # processes completed successfully
    assert exitcode == 0

    stripped = out.strip()
    split = re.split(r'\s+', stripped) if stripped else []
    output_numbers = set([int(n) for n in split])
    logged_numbers = set(range(shell.attrs["count"]))

    # 0 is always output if logger.force_echo() works
    assert 0 in output_numbers

    # no unexpected numbers
    assert output_numbers <= logged_numbers

    # only numbers between v presses are output (this tests whether some
    # of the numbers were hidden, i.e., when verbose was off.
    assert len(output_numbers) < len(logged_numbers)
