# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import argparse
import io
from typing import List, Optional

import spack.cmd
import spack.environment as ev
import spack.llnl.util.tty as tty
import spack.spec
import spack.store
import spack.verify
import spack.verify_libraries
from spack.cmd.common import arguments
from spack.llnl.string import plural
from spack.llnl.util.filesystem import visit_directory_tree

description = "verify spack installations on disk"
section = "admin"
level = "long"

MANIFEST_SUBPARSER: Optional[argparse.ArgumentParser] = None


def setup_parser(subparser: argparse.ArgumentParser):
    global MANIFEST_SUBPARSER
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="verify_command")

    MANIFEST_SUBPARSER = sp.add_parser(
        "manifest", help=verify_manifest.__doc__, description=verify_manifest.__doc__
    )
    MANIFEST_SUBPARSER.add_argument(
        "-l", "--local", action="store_true", help="verify only locally installed packages"
    )
    MANIFEST_SUBPARSER.add_argument(
        "-j", "--json", action="store_true", help="ouptut json-formatted errors"
    )
    MANIFEST_SUBPARSER.add_argument("-a", "--all", action="store_true", help="verify all packages")
    MANIFEST_SUBPARSER.add_argument(
        "specs_or_files", nargs=argparse.REMAINDER, help="specs or files to verify"
    )

    manifest_sp_type = MANIFEST_SUBPARSER.add_mutually_exclusive_group()
    manifest_sp_type.add_argument(
        "-s",
        "--specs",
        action="store_const",
        const="specs",
        dest="type",
        default="specs",
        help="treat entries as specs (default)",
    )
    manifest_sp_type.add_argument(
        "-f",
        "--files",
        action="store_const",
        const="files",
        dest="type",
        default="specs",
        help="treat entries as absolute filenames\n\ncannot be used with '-a'",
    )

    libraries_subparser = sp.add_parser(
        "libraries", help=verify_libraries.__doc__, description=verify_libraries.__doc__
    )

    arguments.add_common_arguments(libraries_subparser, ["constraint"])

    versions_subparser = sp.add_parser(
        "versions", help=verify_versions.__doc__, description=verify_versions.__doc__
    )
    arguments.add_common_arguments(versions_subparser, ["constraint"])


def verify(parser, args):
    cmd = args.verify_command
    if cmd == "libraries":
        return verify_libraries(args)
    elif cmd == "manifest":
        return verify_manifest(args)
    elif cmd == "versions":
        return verify_versions(args)
    parser.error("invalid verify subcommand")


def verify_versions(args):
    """Check that all versions of installed packages are known to Spack and non-deprecated.

    Reports errors for any of the following:

    1. Installed package not loadable from the repo
    2. Installed package version not known by the package recipe
    3. Installed package version deprecated in the package recipe
    """
    if args.specs:
        specs = args.specs(installed=True)
    else:
        specs = spack.store.db.query(installed=True)

    msg_lines = _verify_version(specs)
    if msg_lines:
        tty.die("\n".join(msg_lines))


def _verify_version(specs):
    """Helper method for verify_versions."""
    missing_package = []
    unknown_version = []
    deprecated_version = []

    for spec in specs:
        try:
            pkg = spec.package
        except Exception as e:
            tty.debug(str(e))
            missing_package.append(spec)
            continue

        if spec.version not in pkg.versions:
            unknown_version.append(spec)
            continue

        if pkg.versions[spec.version].get("deprecated", False):
            deprecated_version.append(spec)

    msg_lines = []
    if missing_package or unknown_version or deprecated_version:
        errors = len(missing_package) + len(unknown_version) + len(deprecated_version)
        msg_lines = [f"{errors} installed packages have unknown/deprecated versions\n"]

        msg_lines += [
            f"    Cannot check version for {spec} at {spec.prefix}. Cannot load package."
            for spec in missing_package
        ]
        msg_lines += [
            f"    Spec {spec} at {spec.prefix} has version {spec.version} unknown to Spack."
            for spec in unknown_version
        ]
        msg_lines += [
            f"    Spec {spec} at {spec.prefix} has deprecated version {spec.version}."
            for spec in deprecated_version
        ]

    return msg_lines


def verify_libraries(args):
    """verify that shared libraries of install packages can be located in rpaths (Linux only)"""
    specs_from_db = [s for s in args.specs(installed=True) if not s.external]

    tty.info(f"Checking {len(specs_from_db)} packages for shared library resolution")

    errors = 0
    for spec in specs_from_db:
        try:
            pkg = spec.package
        except Exception:
            tty.warn(f"Skipping {spec.cformat('{name}{@version}{/hash}')} due to missing package")
        error_msg = _verify_libraries(spec, pkg.unresolved_libraries)
        if error_msg is not None:
            errors += 1
            tty.error(error_msg)

    if errors:
        tty.error(f"Cannot resolve shared libraries in {plural(errors, 'package')}")
        return 1


def _verify_libraries(spec: spack.spec.Spec, unresolved_libraries: List[str]) -> Optional[str]:
    """Go over the prefix of the installed spec and verify its shared libraries can be resolved."""
    visitor = spack.verify_libraries.ResolveSharedElfLibDepsVisitor(
        [*spack.verify_libraries.ALLOW_UNRESOLVED, *unresolved_libraries]
    )
    visit_directory_tree(spec.prefix, visitor)

    if not visitor.problems:
        return None

    output = io.StringIO()
    visitor.write(output, indent=4, brief=True)
    message = output.getvalue().rstrip()
    return f"{spec.cformat('{name}{@version}{/hash}')}: {spec.prefix}:\n{message}"


def verify_manifest(args):
    """verify that install directories have not been modified since installation"""
    local = args.local

    if args.type == "files":
        if args.all:
            MANIFEST_SUBPARSER.error("cannot use --all with --files")

        for file in args.specs_or_files:
            results = spack.verify.check_file_manifest(file)
            if results.has_errors():
                if args.json:
                    print(results.json_string())
                else:
                    print(results)

        return 0
    else:
        spec_args = spack.cmd.parse_specs(args.specs_or_files)

    if args.all:
        query = spack.store.STORE.db.query_local if local else spack.store.STORE.db.query

        # construct spec list
        if spec_args:
            spec_list = spack.cmd.parse_specs(args.specs_or_files)
            specs = []
            for spec in spec_list:
                specs += query(spec, installed=True)
        else:
            specs = query(installed=True)

    elif args.specs_or_files:
        # construct disambiguated spec list
        env = ev.active_environment()
        specs = list(map(lambda x: spack.cmd.disambiguate_spec(x, env, local=local), spec_args))
    else:
        MANIFEST_SUBPARSER.error("use --all or specify specs to verify")

    for spec in specs:
        tty.debug("Verifying package %s")
        results = spack.verify.check_spec_manifest(spec)
        if results.has_errors():
            if args.json:
                print(results.json_string())
            else:
                tty.msg("In package %s" % spec.format("{name}/{hash:7}"))
                print(results)
            return 1
        else:
            tty.debug(results)
