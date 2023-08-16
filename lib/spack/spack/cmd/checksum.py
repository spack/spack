# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import re
import sys

import llnl.util.lang
from llnl.util import tty

import spack.cmd
import spack.repo
import spack.spec
import spack.stage
import spack.util.crypto
from spack.cmd.common import arguments
from spack.package_base import PackageBase, deprecated_version, preferred_version
from spack.util.editor import editor
from spack.util.format import get_version_lines
from spack.util.naming import valid_fully_qualified_module_name
from spack.version import Version

description = "checksum available versions of a package"
section = "packaging"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        "--keep-stage",
        action="store_true",
        default=False,
        help="don't clean up staging area when command completes",
    )
    subparser.add_argument(
        "-b",
        "--batch",
        action="store_true",
        default=False,
        help="don't ask which versions to checksum",
    )
    subparser.add_argument(
        "-l",
        "--latest",
        action="store_true",
        default=False,
        help="checksum the latest available version",
    )
    subparser.add_argument(
        "-p",
        "--preferred",
        action="store_true",
        default=False,
        help="checksum the known Spack preferred version",
    )
    modes_parser = subparser.add_mutually_exclusive_group()
    modes_parser.add_argument(
        "-a",
        "--add-to-package",
        action="store_true",
        default=False,
        help="add new versions to package",
    )
    modes_parser.add_argument(
        "--verify", action="store_true", default=False, help="verify known package checksums"
    )
    arguments.add_common_arguments(subparser, ["package"])
    subparser.add_argument(
        "versions", nargs=argparse.REMAINDER, help="versions to generate checksums for"
    )


def checksum(parser, args):
    # Did the user pass 'package@version' string?
    if len(args.versions) == 0 and "@" in args.package:
        args.versions = [args.package.split("@")[1]]
        args.package = args.package.split("@")[0]

    # Make sure the user provided a package and not a URL
    if not valid_fully_qualified_module_name(args.package):
        tty.die("`spack checksum` accepts package names, not URLs.")

    # Get the package we're going to generate checksums for
    pkg_cls = spack.repo.PATH.get_pkg_class(args.package)
    pkg = pkg_cls(spack.spec.Spec(args.package))

    # Build a list of versions to checksum
    versions = [Version(v) for v in args.versions]

    # Define placeholder for remote versions.
    # This'll help reduce redundant work if we need to check for the existance
    # of remote versions more than once.
    remote_versions = None

    # Add latest version if requested
    if args.latest:
        remote_versions = pkg.fetch_remote_versions()
        if len(remote_versions) > 0:
            latest_version = sorted(remote_versions.keys(), reverse=True)[0]
            versions.append(latest_version)

    # Add preferred version if requested
    if args.preferred:
        versions.append(preferred_version(pkg))

    # Store a dict of the form version -> URL
    url_dict = {}

    for version in versions:
        if deprecated_version(pkg, version):
            tty.warn(f"Version {version} is deprecated")

        url = pkg.find_valid_url_for_version(version)
        if url is not None:
            url_dict[version] = url
            continue
        # if we get here, it's because no valid url was provided by the package
        # do expensive fallback to try to recover
        if remote_versions is None:
            remote_versions = pkg.fetch_remote_versions()
        if version in remote_versions:
            url_dict[version] = remote_versions[version]

    if len(versions) <= 0:
        if remote_versions is None:
            remote_versions = pkg.fetch_remote_versions()
        url_dict = remote_versions

    if not url_dict:
        tty.die(f"Could not find any remote versions for {pkg.name}")

    # print an empty line to create a new output section block
    print()

    version_hashes = spack.stage.get_checksums_for_versions(
        url_dict,
        pkg.name,
        keep_stage=args.keep_stage,
        batch=(args.batch or len(versions) > 0 or len(url_dict) == 1),
        fetch_options=pkg.fetch_options,
    )

    if args.verify:
        print_checksum_status(pkg, version_hashes)
        sys.exit(0)

    # convert dict into package.py version statements
    version_lines = get_version_lines(version_hashes, url_dict)
    print()
    print(version_lines)
    print()

    if args.add_to_package:
        add_versions_to_package(pkg, version_lines)


def print_checksum_status(pkg: PackageBase, version_hashes: dict):
    """
    Verify checksums present in version_hashes against those present
    in the package's instructions.

    Args:
        pkg (spack.package_base.PackageBase): A package class for a given package in Spack.
        version_hashes (dict): A dictionary of the form: version -> checksum.

    """
    results = []
    num_verified = 0
    failed = False

    max_len = max(len(str(v)) for v in version_hashes)
    num_total = len(version_hashes)

    for version, sha in version_hashes.items():
        if version not in pkg.versions:
            msg = "No previous checksum"
            status = "-"

        elif sha == pkg.versions[version]["sha256"]:
            msg = "Correct"
            status = "="
            num_verified += 1

        else:
            msg = sha
            status = "x"
            failed = True

        results.append("{0:{1}}  {2} {3}".format(str(version), max_len, f"[{status}]", msg))

    # Display table of checksum results.
    tty.msg(f"Verified {num_verified} of {num_total}", "", *llnl.util.lang.elide_list(results), "")

    # Terminate at the end of function to prevent additional output.
    if failed:
        print()
        tty.die("Invalid checksums found.")


def add_versions_to_package(pkg: PackageBase, version_lines: str):
    """
    Add checksumed versions to a package's instructions and open a user's
    editor so they may double check the work of the function.

    Args:
        pkg (spack.package_base.PackageBase): A package class for a given package in Spack.
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
                    split_contents[i:i] = [new_versions.pop(0)[1], " # FIX ME", "\n"]
                    num_versions_added += 1

                elif parsed_version == new_versions[0][0]:
                    new_versions.pop(0)

        # Seek back to the start of the file so we can rewrite the file contents.
        f.seek(0)
        f.writelines("".join(split_contents))

        tty.msg(f"Added {num_versions_added} new versions to {pkg.name}")
        tty.msg(f"Open {filename} to review the additions.")

    if sys.stdout.isatty():
        editor(filename)
