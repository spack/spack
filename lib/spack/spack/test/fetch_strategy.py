# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from io import StringIO

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


def test_fetch_progress_unknown_size():
    # time stamps in seconds, with 0.1s delta except 1.5 -> 1.55.
    time_stamps = iter([1.0, 1.5, 1.55, 2.0, 3.0, 5.0, 5.5, 5.5])
    progress = fetch_strategy.FetchProgress(total_bytes=None, get_time=lambda: next(time_stamps))
    assert progress.start_time == 1.0
    out = StringIO()

    progress.advance(1000, out)
    assert progress.last_printed == 1.5
    progress.advance(50, out)
    assert progress.last_printed == 1.5  # does not print, too early after last print
    progress.advance(2000, out)
    assert progress.last_printed == 2.0
    progress.advance(3000, out)
    assert progress.last_printed == 3.0
    progress.advance(4000, out)
    assert progress.last_printed == 5.0
    progress.advance(4000, out)
    assert progress.last_printed == 5.5
    progress.print(final=True, out=out)  # finalize download

    outputs = [
        "\r    [ |  ]    1.00 KB @    2.0 KB/s",
        "\r    [ /  ]    3.05 KB @    3.0 KB/s",
        "\r    [ -  ]    6.05 KB @    3.0 KB/s",
        "\r    [ \\  ]   10.05 KB @    2.5 KB/s",  # have to escape \ here but is aligned in output
        "\r    [ |  ]   14.05 KB @    3.1 KB/s",
        "\r    [100%]   14.05 KB @    3.1 KB/s\n",  # final print: no spinner; newline
    ]

    assert out.getvalue() == "".join(outputs)


def test_fetch_progress_known_size():
    time_stamps = iter([1.0, 1.5, 3.0, 4.0, 4.0])
    progress = fetch_strategy.FetchProgress(total_bytes=6000, get_time=lambda: next(time_stamps))
    out = StringIO()
    progress.advance(1000, out)  # time 1.5
    progress.advance(2000, out)  # time 3.0
    progress.advance(3000, out)  # time 4.0
    progress.print(final=True, out=out)

    outputs = [
        "\r    [ 17%]    1.00 KB @    2.0 KB/s",
        "\r    [ 50%]    3.00 KB @    1.5 KB/s",
        "\r    [100%]    6.00 KB @    2.0 KB/s",
        "\r    [100%]    6.00 KB @    2.0 KB/s\n",  # final print has newline
    ]

    assert out.getvalue() == "".join(outputs)


def test_fetch_progress_disabled():
    """When disabled, FetchProgress shouldn't print anything when advanced"""

    def get_time():
        raise RuntimeError("Should not be called")

    progress = fetch_strategy.FetchProgress(enabled=False, get_time=get_time)
    out = StringIO()
    progress.advance(1000, out)
    progress.advance(2000, out)
    progress.print(final=True, out=out)
    assert progress.last_printed == 0
    assert not out.getvalue()


@pytest.mark.parametrize(
    "header,value,total_bytes",
    [
        ("Content-Length", "1234", 1234),
        ("Content-Length", "0", 0),
        ("Content-Length", "-10", 0),
        ("Content-Length", "not a number", 0),
        ("Not-Content-Length", "1234", 0),
    ],
)
def test_fetch_progress_from_headers(header, value, total_bytes):
    time_stamps = iter([1.0, 1.5, 3.0, 4.0, 4.0])
    progress = fetch_strategy.FetchProgress.from_headers(
        {header: value}, get_time=lambda: next(time_stamps), enabled=True
    )
    assert progress.total_bytes == total_bytes
    assert progress.enabled
    assert progress.start_time == 1.0


def test_fetch_progress_from_headers_disabled():
    progress = fetch_strategy.FetchProgress.from_headers(
        {"Content-Length": "1234"}, get_time=lambda: 1.0, enabled=False
    )
    assert not progress.enabled
