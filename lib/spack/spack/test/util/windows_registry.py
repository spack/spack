# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for ``util/windows_registry.py``."""

import sys

import pytest

if sys.platform != "win32":
    pytest.skip("Windows-only tests", allow_module_level=True)

from spack.util.windows_registry import HKEY, WindowsRegistryView


@pytest.fixture
def software_key():
    """A registry key that is guaranteed to exist on any Windows host."""
    return WindowsRegistryView("SOFTWARE\\Microsoft", root_key=HKEY.HKEY_LOCAL_MACHINE)


def test_find_subkeys_returns_empty_list_when_nothing_matches(software_key):
    """find_subkeys must return a list, not None, so callers can iterate unconditionally.

    Regression test: a host without Visual Studio has no ``VisualStudio_*`` subkeys, which
    made ``spack.operating_systems.windows_os`` raise ``TypeError: 'NoneType' object is not
    iterable`` while detecting compilers.
    """
    assert software_key.find_subkeys("ThisSubkeyDoesNotExist_.*", recursive=False) == []


def test_find_subkeys_returns_matches(software_key):
    matches = software_key.find_subkeys("Window.*", recursive=False)
    assert isinstance(matches, list)
    assert all(key.name.startswith("Window") for key in matches)
