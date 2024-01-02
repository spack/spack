# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from typing import Optional


def get_version_lines(version_hashes_dict: dict, url_dict: Optional[dict] = None) -> str:
    """
    Renders out a set of versions like those found in a package's
    package.py file for a given set of versions and hashes.

    Args:
        version_hashes_dict (dict): A dictionary of the form: version -> checksum.
        url_dict (dict): A dictionary of the form: version -> URL.

    Returns:
        (str): Rendered version lines.
    """
    version_lines = []

    for v, h in version_hashes_dict.items():
        expand_arg = ""

        # Extract the url for a version if url_dict is provided.
        url = ""
        if url_dict is not None and v in url_dict:
            url = url_dict[v]

        # Add expand_arg since wheels should not be expanded during stanging
        if url.endswith(".whl") or ".whl#" in url:
            expand_arg = ", expand=False"
        version_lines.append(f'    version("{v}", sha256="{h}"{expand_arg})')

    return "\n".join(version_lines)
