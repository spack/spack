# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Unit tests for the platform-independent sandbox interface."""

import pathlib
from typing import List, Tuple

import pytest

import spack.sandbox_base


class MockSandbox(spack.sandbox_base.Sandbox):
    def __init__(self):
        self.read_calls: List[Tuple[pathlib.Path, pathlib.Path]] = []

    def _allow_read(self, original: pathlib.Path, resolved: pathlib.Path):
        self.read_calls.append((original, resolved))

    def _allow_write(self, original: pathlib.Path, resolved: pathlib.Path):
        pass

    def apply(self, block_network=False):
        pass


def test_allow_read_reports_both_the_requested_and_resolved_path(tmp_path: pathlib.Path):
    """Backends need the resolved path to apply a rule, and the original to report on it.

    Rules are keyed by resolved path so that two names for one directory collapse to a single
    rule instead of racing each other.
    """
    target = tmp_path / "target"
    target.mkdir()
    link = tmp_path / "link"
    try:
        link.symlink_to(target)
    except OSError as e:
        # Windows only permits this under Developer Mode or with elevation.
        pytest.skip(f"cannot create symlinks on this host: {e}")

    sandbox = MockSandbox()
    sandbox.allow_read(link)

    assert sandbox.read_calls == [(link.absolute(), target.resolve())]
