# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from typing import Mapping, Optional

INDENT = " " * 4


def get_version_lines(
    version_hashes_dict: Mapping, url_changed_for_version: Optional[Mapping] = None
) -> str:
    """
    Renders out a set of versions like those found in a package's
    package.py file for a given set of versions and hashes.

    Args:
        version_hashes_dict: A dictionary of the form: version -> checksum.
        url_changed_for_version: A dictionary of the form: version -> url.

    Returns: Rendered version lines.
    """
    url_overrides = url_changed_for_version or {}
    version_lines = []

    for version in sorted(version_hashes_dict):
        checksum = version_hashes_dict[version]

        url = url_overrides.get(version)
        url_parameter = f', url="{url}"' if url is not None else ""

        line = f'{INDENT}version("{version}", sha256="{checksum}"{url_parameter})'
        version_lines.append(line)

    return "\n".join(version_lines)
