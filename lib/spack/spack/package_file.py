# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import spack.repo
from spack.package_base import PackageBase
from spack.version import Version


def add_versions_to_package(pkg: PackageBase, version_lines: str):
    """
    Add checksumed versions to a package's instructions and open a user's
    editor so they may double check the work of the function.

    Args:
        pkg (spack.package_base.PackageBase): A package class for a program.
        version_lines (str): A string of rendered version lines.

    """
    # Get filename and path for package
    filename = spack.repo.PATH.filename_for_package_name(pkg.name)
    num_versions_added = 0

    version_statement_re = re.compile(r"([\t ]+version\([^\)]*\))")
    version_re = re.compile(r'[\t ]+version\(\s*"([^"]+)"[^\)]*\)')

    # Split rendered version lines into tuple of (version, version_line)
    # We reverse sort here to make sure the versions match the version_lines
    new_versions = []
    for ver_line in version_lines.split("\n"):
        match = version_re.match(ver_line)
        if match:
            new_versions.append((Version(match.group(1)), ver_line))

    with open(filename, "r+") as f:
        contents = f.read()
        split_contents = version_statement_re.split(contents)

        for i, subsection in enumerate(split_contents):
            # If there are no more versions to add we should exit
            if len(new_versions) <= 0:
                break

            # Check if the section contains a version
            contents_version = version_re.match(subsection)
            if contents_version is not None:
                parsed_version = Version(contents_version.group(1))

                if parsed_version < new_versions[0][0]:
                    split_contents[i:i] = [new_versions.pop(0)[1], "\n"]
                    num_versions_added += 1

                elif parsed_version == new_versions[0][0]:
                    new_versions.pop(0)

        # Seek back to the start of the file so we can rewrite the file contents.
        f.seek(0)
        f.writelines("".join(split_contents))

    return num_versions_added
