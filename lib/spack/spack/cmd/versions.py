# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import sys
from typing import Any, Dict, Set

import spack.llnl.util.tty as tty
import spack.repo
import spack.spec
from spack.cmd.common import arguments
from spack.llnl.util.tty.colify import colify
from spack.version import StandardVersion

description = "list available versions of a package"
section = "query"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    output = subparser.add_mutually_exclusive_group()
    output.add_argument(
        "-s", "--safe", action="store_true", help="only list safe versions of the package"
    )
    output.add_argument(
        "-r", "--remote", action="store_true", help="only list remote versions of the package"
    )
    output.add_argument(
        "-n",
        "--new",
        action="store_true",
        help="only list remote versions newer than the checksummed versions",
    )
    arguments.add_common_arguments(subparser, ["package", "jobs"])


def new_versions(
    safe_versions: Dict[StandardVersion, Any], fetched_versions: Dict[StandardVersion, Any]
) -> Set[StandardVersion]:
    """Return the newest remote version in each version prefix branch not yet checksummed.

    For every unique component-prefix derived from ``safe_versions`` (plus the empty prefix that
    catches entirely new major series), pick the largest version in ``fetched_versions`` whose
    release tuple starts with that prefix. Versions already in ``safe_versions`` are excluded.

    For example, if the versions {3.14.3, 3.13.1} are checksummed, their corresponding prefixes
    are the set ``{(), (3,), (3, 14), (3, 13)}``. From those, remote candidates
    ``{4.0.0, 3.15.0, 3.14.4, 3.13.2}`` would be returned (new major, minor and patch versions).
    """
    numeric_safe = [v for v in safe_versions if not v.isdevelop()]
    fetched_list = sorted((v for v in fetched_versions if not v.isdevelop()), reverse=True)

    # Prefixes of the form (3,), (3, 14), etc.
    prefixes: Set[tuple] = {
        v.version[0][:n] for v in numeric_safe for n in range(1, len(v.version[0]))
    }
    # Look for new major versions (empty prefix).
    prefixes.add(())

    result: Set[StandardVersion] = set()
    for prefix in prefixes:
        n = len(prefix)
        for v in fetched_list:
            if v.version[0][:n] == prefix:
                if v not in safe_versions:
                    result.add(v)
                break
    return result


def versions(parser, args):
    spec = spack.spec.Spec(args.package)
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
    pkg = pkg_cls(spec)

    safe_versions = pkg.versions

    if not (args.remote or args.new):
        if sys.stdout.isatty():
            tty.msg("Safe versions (already checksummed):")

        if not safe_versions:
            if sys.stdout.isatty():
                tty.warn(f"Found no versions for {pkg.name}")
                tty.debug("Manually add versions to the package.")
        else:
            colify(sorted(safe_versions, reverse=True), indent=2)

        if args.safe:
            return

    fetched_versions = pkg.fetch_remote_versions(args.jobs)

    if args.new:
        if sys.stdout.isatty():
            tty.msg("New remote versions (not yet checksummed):")
        remote_versions = new_versions(safe_versions, fetched_versions)
    else:
        if sys.stdout.isatty():
            tty.msg("Remote versions (not yet checksummed):")
        remote_versions = set(fetched_versions).difference(safe_versions)

    if not remote_versions:
        if sys.stdout.isatty():
            if not fetched_versions:
                tty.warn(f"Found no versions for {pkg.name}")
                tty.debug(
                    "Check the list_url and list_depth attributes of "
                    "the package to help Spack find versions."
                )
            else:
                tty.warn(f"Found no unchecksummed versions for {pkg.name}")
    else:
        colify(sorted(remote_versions, reverse=True), indent=2)
