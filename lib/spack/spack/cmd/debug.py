# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import platform
import re
from typing import Optional

import spack
import spack.cmd
import spack.config
import spack.debug_source
from spack.active_environment import active_environment
import spack.platforms
import spack.repo
import spack.spec
import spack.util.git
from spack.util import tty

description = "debugging commands for troubleshooting Spack"
section = "developer"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="debug_command")
    sp.add_parser("report", help="print information useful for bug reports")

    stage_source_parser = sp.add_parser(
        "stage-source",
        help="fetch pristine source for an installed package into the debug-source cache "
        "(fallback for packages installed without 'spack install --debug-source')",
    )
    stage_source_parser.add_argument("spec", help="installed spec to stage source for")
    stage_source_parser.add_argument(
        "--force", action="store_true", help="re-stage even if already staged"
    )

    split_symbols_parser = sp.add_parser(
        "split-symbols",
        help="split debug symbols for an installed package into the debug-source cache "
        "(fallback for packages installed without 'spack install --debug-symbols')",
    )
    split_symbols_parser.add_argument("spec", help="installed spec to split symbols for")
    split_symbols_parser.add_argument(
        "--force", action="store_true", help="re-split even if already split"
    )

def _format_repo_info(source, commit):
    if source.endswith(".git"):
        return f"{source[:-4]}/commit/{commit}"

    return f"{source} ({commit[:7]})"


def _get_builtin_repo_info() -> Optional[str]:
    """Get the builtin package repository git commit sha."""
    # Get builtin from config
    descriptors = spack.repo.RepoDescriptors.from_config(
        spack.repo.package_repository_lock(), spack.config.CONFIG
    )
    if "builtin" not in descriptors:
        return None

    builtin = descriptors["builtin"]

    source = None
    if isinstance(builtin, spack.repo.RemoteRepoDescriptor) and builtin.fetched():
        destination = builtin.destination
        source = builtin.repository
    elif isinstance(builtin, spack.repo.LocalRepoDescriptor):
        destination = builtin.path
        source = builtin.path
    else:
        return None  # no git info

    git = spack.util.git.git(required=False)
    if not git:
        return None

    rev = git(
        "-C", destination, "rev-parse", "HEAD", output=str, error=os.devnull, fail_on_error=False
    )
    if git.returncode != 0:
        return None

    match = re.match(r"[a-f\d]{7,}$", rev)
    return _format_repo_info(source, match.group(0)) if match else None


def _get_spack_repo_info() -> str:
    """Get the spack package repository git info."""
    commit = spack.get_spack_commit()
    if not commit:
        return spack.spack_version

    repo_info = _format_repo_info("https://github.com/spack/spack.git", commit)
    return f"{spack.spack_version} ({repo_info})"


def report(args):
    host_platform = spack.platforms.host()
    host_os = host_platform.default_operating_system()
    host_target = host_platform.default_target()
    architecture = spack.spec.ArchSpec((str(host_platform), str(host_os), str(host_target)))
    print("* **Spack:**", _get_spack_repo_info())
    print("* **Builtin repo:**", _get_builtin_repo_info() or "not available")
    print("* **Python:**", platform.python_version())
    print("* **Platform:**", architecture)


def stage_source(args):
    specs = spack.cmd.parse_specs(args.spec, concretize=False)
    if len(specs) != 1:
        tty.die("'spack debug stage-source' requires exactly one spec")

    env = active_environment()
    spec = spack.cmd.disambiguate_spec(specs[0], env)
    pkg = spec.package
    spack.debug_source.stage_source(pkg, force=args.force)


def split_symbols(args):
    specs = spack.cmd.parse_specs(args.spec, concretize=False)
    if len(specs) != 1:
        tty.die("'spack debug split-symbols' requires exactly one spec")

    env = active_environment()
    spec = spack.cmd.disambiguate_spec(specs[0], env)
    pkg = spec.package
    spack.debug_source.split_symbols(pkg, force=args.force)


def debug(parser, args):
    if args.debug_command == "report":
        report(args)
    elif args.debug_command == "stage-source":
        stage_source(args)
    elif args.debug_command == "split-symbols":
        split_symbols(args)
