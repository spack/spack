# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import platform
import re
from typing import Optional

import spack
import spack.config
import spack.platforms
import spack.repo
import spack.spec
import spack.util.git

description = "debugging commands for troubleshooting Spack"
section = "developer"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="debug_command")
    sp.add_parser("report", help="print information useful for bug reports")


def _get_builtin_repo_commit() -> Optional[str]:
    """Get the builtin package repository git commit sha."""
    # Get builtin from config
    descriptors = spack.repo.RepoDescriptors.from_config(
        spack.repo.package_repository_lock(), spack.config.CONFIG
    )

    if "builtin" not in descriptors:
        return None

    builtin = descriptors["builtin"]

    if not isinstance(builtin, spack.repo.RemoteRepoDescriptor) or not builtin.fetched():
        return None  # no git info

    git = spack.util.git.git(required=False)
    if not git:
        return None

    rev = git(
        "-C",
        builtin.destination,
        "rev-parse",
        "HEAD",
        output=str,
        error=os.devnull,
        fail_on_error=False,
    )
    if git.returncode != 0:
        return None

    match = re.match(r"[a-f\d]{7,}$", rev)
    return match.group(0) if match else None


def report(args):
    host_platform = spack.platforms.host()
    host_os = host_platform.default_operating_system()
    host_target = host_platform.default_target()
    architecture = spack.spec.ArchSpec((str(host_platform), str(host_os), str(host_target)))
    print("* **Spack:**", spack.get_version())
    print("* **Builtin repo:**", _get_builtin_repo_commit() or "not available")
    print("* **Python:**", platform.python_version())
    print("* **Platform:**", architecture)


def debug(parser, args):
    if args.debug_command == "report":
        report(args)
