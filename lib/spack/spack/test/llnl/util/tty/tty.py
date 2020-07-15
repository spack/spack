# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty


def test_get_timestamp():
    """Ensure the results of get_timestamp are reasonable."""

    # Debug disabled should return an empty string
    tty._debug = tty.DISABLED
    assert not tty.get_timestamp(False), 'Expected an empty string'

    # Debug disabled but force the timestamp should return a string
    assert tty.get_timestamp(True), 'Expected a timestamp/non-empty string'

    pid_str = ' {0}'.format(os.getpid())

    # Basic debugging should return a timestamp sans pid
    tty._debug = tty.BASIC
    out_str = tty.get_timestamp(False)
    assert out_str and pid_str not in out_str, 'Expected no PID in results'

    # Standard debugging should return a timestamp WITH the pid
    tty._debug = tty.STANDARD
    out_str = tty.get_timestamp(False)
    assert out_str and pid_str in out_str, 'Expected PID in results'

    # Detailed debugging should return a timestamp WITH the pid
    tty._debug = tty.DETAILED
    out_str = tty.get_timestamp(False)
    assert out_str and pid_str in out_str, 'Expected PID in results'
