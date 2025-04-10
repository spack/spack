# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from spack import fetch_strategy


def test_fetchstrategy_bad_url_scheme():
    """Ensure that trying to make a fetch strategy from a URL with an
    unsupported scheme fails as expected."""

    with pytest.raises(ValueError):
        fetcher = fetch_strategy.from_url_scheme("bogus-scheme://example.com/a/b/c")  # noqa: F841


@pytest.mark.parametrize(
    "expected,total_bytes",
    [
        ("   0.00  B", 0),
        (" 999.00  B", 999),
        ("   1.00 KB", 1000),
        ("   2.05 KB", 2048),
        ("   1.00 MB", 1e6),
        ("  12.30 MB", 1.23e7),
        ("   1.23 GB", 1.23e9),
        (" 999.99 GB", 9.9999e11),
        ("5000.00 GB", 5e12),
    ],
)
def test_format_bytes(expected, total_bytes):
    assert fetch_strategy._format_bytes(total_bytes) == expected


@pytest.mark.parametrize(
    "expected,total_bytes,elapsed",
    [
        ("   0.0  B/s", 0, 0),  # no time passed -- defaults to 1s.
        ("   0.0  B/s", 0, 1),
        (" 999.0  B/s", 999, 1),
        ("   1.0 KB/s", 1000, 1),
        (" 500.0  B/s", 1000, 2),
        ("   2.0 KB/s", 2048, 1),
        ("   1.0 MB/s", 1e6, 1),
        (" 500.0 KB/s", 1e6, 2),
        ("  12.3 MB/s", 1.23e7, 1),
        ("   1.2 GB/s", 1.23e9, 1),
        (" 999.9 GB/s", 9.999e11, 1),
        ("5000.0 GB/s", 5e12, 1),
    ],
)
def test_format_speed(expected, total_bytes, elapsed):
    assert fetch_strategy._format_speed(total_bytes, elapsed) == expected
