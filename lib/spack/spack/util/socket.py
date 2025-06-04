# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Optimized Spack implementations of methods from socket module."""

import socket

import llnl.util.lang


@llnl.util.lang.memoized
def _getfqdn():
    """Memoized version of `getfqdn()`.

    If we call `getfqdn()` too many times, DNS can be very slow. We only need to call it
    one time per process, so we cache it here.

    """
    return socket.getfqdn()
