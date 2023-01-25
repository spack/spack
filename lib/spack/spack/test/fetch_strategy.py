# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from spack import fetch_strategy


def test_fetchstrategy_bad_url_scheme():
    """Ensure that trying to make a fetch strategy from a URL with an
    unsupported scheme fails as expected."""

    with pytest.raises(ValueError):
        fetcher = fetch_strategy.from_url_scheme("bogus-scheme://example.com/a/b/c")  # noqa: F841


def test_filesummary(tmpdir):
    p = str(tmpdir.join("xyz"))
    with open(p, "wb") as f:
        f.write(b"abcdefghijklmnopqrstuvwxyz")

    assert fetch_strategy._filesummary(p, print_bytes=8) == (26, b"abcdefgh...stuvwxyz")
    assert fetch_strategy._filesummary(p, print_bytes=13) == (26, b"abcdefghijklmnopqrstuvwxyz")
    assert fetch_strategy._filesummary(p, print_bytes=100) == (26, b"abcdefghijklmnopqrstuvwxyz")
