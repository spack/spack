# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


def get_version_lines(version_hashes_dict: dict) -> str:
    """
    Renders out a set of versions like those found in a package's
    package.py file for a given set of versions and hashes.

    Args:
        version_hashes_dict: A dictionary of the form: version -> checksum.

    Returns: Rendered version lines.
    """
    version_lines = []

    for v, h in version_hashes_dict.items():
        version_lines.append(f'    version("{v}", sha256="{h}")')

    return "\n".join(version_lines)
