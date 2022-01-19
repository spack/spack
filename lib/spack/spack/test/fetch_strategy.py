# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from spack.fetch_strategy import from_url_scheme


def test_fetchstrategy_bad_url_scheme():
    """Ensure that trying to make a fetch strategy from a URL with an
    unsupported scheme fails as expected."""

    with pytest.raises(ValueError):
        fetcher = from_url_scheme(  # noqa: F841
            'bogus-scheme://example.com/a/b/c')
