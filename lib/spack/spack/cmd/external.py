# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from __future__ import print_function

import argparse
import errno
import os
import sys

import llnl.util.tty as tty
import llnl.util.tty.colify as colify

import spack
import spack.cmd
import spack.cmd.common.arguments
import spack.cray_manifest as cray_manifest
import spack.detection
import spack.error
import spack.util.environment

description = "manage external packages in Spack configuration"
section = "config"
level = "short"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="external_command")

    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    find_parser = sp.add_parser("find", help="add external packages to packages.yaml")
    find_parser.add_argument(
        "--not-buildable",
        action="store_true",
        default=False,
        help="packages with detected externals won't be built with Spack",
    )
    find_parser.add_argument("--exclude", action="append", help="packages to exclude from search")
    find_parser.add_argument(
        "-p",
        "--path",
        default=None,
        action="append",
        help="Alternative search paths for finding externals. May be repeated",
    )
    find_parser.add_argument(
        "--scope",
        choices=scopes,
        metavar=scopes_metavar,
        default=spack.config.default_modify_scope("packages"),
        help="configuration scope to modify",
    )
    find_parser.add_argument(
        "--all", action="store_true", help="search for all packages that Spack knows about"
    )
    spack.cmd.common.arguments.add_common_arguments(find_parser, ["tags"])
    find_parser.add_argument("packages", nargs=argparse.REMAINDER)
    find_parser.epilog = (
        'The search is by default on packages tagged with the "build-tools" or '
        '"core-packages" tags. Use the --all option to search for every possible '
        "package Spack knows how to find."
    )

    sp.add_parser("list", help="list detectable packages, by repository and name")

    read_cray_manifest = sp.add_parser(
        "read-cray-manifest",
        help=(
            "consume a Spack-compatible description of externally-installed "
            "packages, including dependency relationships"
        ),
    )
    read_cray_manifest.add_argument(
        "--file", default=None, help="specify a location other than the default"
    )
    read_cray_manifest.add_argument(
        "--directory", default=None, help="specify a directory storing a group of manifest files"
    )
    read_cray_manifest.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="don't modify DB with files that are read",
    )
    read_cray_manifest.add_argument(
        "--fail-on-error",
        action="store_true",
        help=("if a manifest file cannot be parsed, fail and report the " "full stack trace"),
    )


def external_find(args):
    if args.all or not (args.tags or args.packages):
        # If the user calls 'spack external find' with no arguments, and
        # this system has a description of installed packages, then we should
        # consume it automatically.
        try:
            _collect_and_consume_cray_manifest_files()
        except NoManifestFileError:
            # It's fine to not find any manifest file if we are doing the
            # search implicitly (i.e. as part of 'spack external find')
            pass
        except Exception as e:
            # For most exceptions, just print a warning and continue.
            # Note that KeyboardInterrupt does not subclass Exception
            # (so CTRL-C will terminate the program as expected).
            skip_msg = "Skipping manifest and continuing with other external " "checks"
            if (isinstance(e, IOError) or isinstance(e, OSError)) and e.errno in [
                errno.EPERM,
                errno.EACCES,
            ]:
                # The manifest file does not have sufficient permissions enabled:
                # print a warning and keep going
                tty.warn("Unable to read manifest due to insufficient " "permissions.", skip_msg)
            else:
                tty.warn("Unable to read manifest, unexpected error: {0}".format(str(e)), skip_msg)

    # If the user didn't specify anything, search for build tools by default
    if not args.tags and not args.all and not args.packages:
        args.tags = ["core-packages", "build-tools"]

    # If the user specified both --all and --tag, then --all has precedence
    if args.all and args.tags:
        args.tags = []

    # Construct the list of possible packages to be detected
    pkg_cls_to_check = []

    # Add the packages that have been required explicitly
    if args.packages:
        pkg_cls_to_check = [spack.repo.path.get_pkg_class(pkg) for pkg in args.packages]
        if args.tags:
            allowed = set(spack.repo.path.packages_with_tags(*args.tags))
            pkg_cls_to_check = [x for x in pkg_cls_to_check if x.name in allowed]

    if args.tags and not pkg_cls_to_check:
        # If we arrived here we didn't have any explicit package passed
        # as argument, which means to search all packages.
        # Since tags are cached it's much faster to construct what we need
        # to search directly, rather than filtering after the fact
        pkg_cls_to_check = [
            spack.repo.path.get_pkg_class(pkg_name)
            for tag in args.tags
            for pkg_name in spack.repo.path.packages_with_tags(tag)
        ]
        pkg_cls_to_check = list(set(pkg_cls_to_check))

    # If the list of packages is empty, search for every possible package
    if not args.tags and not pkg_cls_to_check:
        pkg_cls_to_check = list(spack.repo.path.all_package_classes())

    # If the user specified any packages to exclude from external find, add them here
    if args.exclude:
        pkg_cls_to_check = [pkg for pkg in pkg_cls_to_check if pkg.name not in args.exclude]

    detected_packages = spack.detection.by_executable(pkg_cls_to_check, path_hints=args.path)
    detected_packages.update(spack.detection.by_library(pkg_cls_to_check, path_hints=args.path))

    new_entries = spack.detection.update_configuration(
        detected_packages, scope=args.scope, buildable=not args.not_buildable
    )
    if new_entries:
        path = spack.config.config.get_config_filename(args.scope, "packages")
        msg = "The following specs have been detected on this system " "and added to {0}"
        tty.msg(msg.format(path))
        spack.cmd.display_specs(new_entries)
    else:
        tty.msg("No new external packages detected")


def external_read_cray_manifest(args):
    _collect_and_consume_cray_manifest_files(
        manifest_file=args.file,
        manifest_directory=args.directory,
        dry_run=args.dry_run,
        fail_on_error=args.fail_on_error,
    )


def _collect_and_consume_cray_manifest_files(
    manifest_file=None, manifest_directory=None, dry_run=False, fail_on_error=False
):
    manifest_files = []
    if manifest_file:
        manifest_files.append(manifest_file)

    manifest_dirs = []
    if manifest_directory:
        manifest_dirs.append(manifest_directory)

    if os.path.isdir(cray_manifest.default_path):
        tty.debug(
            "Cray manifest path {0} exists: collecting all files to read.".format(
                cray_manifest.default_path
            )
        )
        manifest_dirs.append(cray_manifest.default_path)
    else:
        tty.debug(
            "Default Cray manifest directory {0} does not exist.".format(
                cray_manifest.default_path
            )
        )

    for directory in manifest_dirs:
        for fname in os.listdir(directory):
            if fname.endswith(".json"):
                fpath = os.path.join(directory, fname)
                tty.debug("Adding manifest file: {0}".format(fpath))
                manifest_files.append(os.path.join(directory, fpath))

    if not manifest_files:
        raise NoManifestFileError(
            "--file/--directory not specified, and no manifest found at {0}".format(
                cray_manifest.default_path
            )
        )

    for path in manifest_files:
        tty.debug("Reading manifest file: " + path)
        try:
            cray_manifest.read(path, not dry_run)
        except spack.error.SpackError as e:
            if fail_on_error:
                raise
            else:
                tty.warn("Failure reading manifest file: {0}" "\n\t{1}".format(path, str(e)))


def external_list(args):
    # Trigger a read of all packages, might take a long time.
    list(spack.repo.path.all_package_classes())
    # Print all the detectable packages
    tty.msg("Detectable packages per repository")
    for namespace, pkgs in sorted(spack.package_base.detectable_packages.items()):
        print("Repository:", namespace)
        colify.colify(pkgs, indent=4, output=sys.stdout)


def external(parser, args):
    action = {
        "find": external_find,
        "list": external_list,
        "read-cray-manifest": external_read_cray_manifest,
    }
    action[args.external_command](args)


class NoManifestFileError(spack.error.SpackError):
    pass
