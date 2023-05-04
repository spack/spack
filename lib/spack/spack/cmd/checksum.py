# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import argparse
import sys

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.repo
import spack.spec
import spack.stage
import spack.util.crypto
from spack.package_base import deprecated_version, preferred_version
from spack.util.editor import editor
from spack.util.naming import valid_fully_qualified_module_name
from spack.version import VersionBase, ver

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
    sp = subparser.add_mutually_exclusive_group()
    sp.add_argument(
        "-b",
        "--batch",
        action="store_true",
        default=False,
        help="don't ask which versions to checksum",
    )
    sp.add_argument(
        "-l",
        "--latest",
        action="store_true",
        default=False,
        help="checksum the latest available version only",
    )
    sp.add_argument(
        "-p",
        "--preferred",
        action="store_true",
        default=False,
        help="checksum the preferred version only",
    )
    subparser.add_argument(
        "-a",
        "--add-to-package",
        action="store_true",
        default=False,
        help="add new versions to package",
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
    pkg_cls = spack.repo.path.get_pkg_class(args.package)
    pkg = pkg_cls(spack.spec.Spec(args.package))

    url_dict = {}
    versions = args.versions
    if (not versions) and args.preferred:
        versions = [preferred_version(pkg)]

    if versions:
        remote_versions = None
        for version in versions:
            if deprecated_version(pkg, version):
                tty.warn("Version {0} is deprecated".format(version))

            version = ver(version)
            if not isinstance(version, VersionBase):
                tty.die(
                    "Cannot generate checksums for version lists or "
                    "version ranges. Use unambiguous versions."
                )
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
    else:
        url_dict = pkg.fetch_remote_versions()

    if not url_dict:
        tty.die("Could not find any remote versions for {0}".format(pkg.name))

    version_lines = spack.stage.get_checksums_for_versions(
        url_dict,
        pkg.name,
        keep_stage=args.keep_stage,
        batch=(args.batch or len(args.versions) > 0 or len(url_dict) == 1),
        latest=args.latest,
        fetch_options=pkg.fetch_options,
    )

    print()
    print(version_lines)
    print()

    if args.add_to_package:
        filename = spack.repo.path.filename_for_package_name(pkg.name)
        # Make sure we also have a newline after the last version
        versions = [v + "\n" for v in version_lines.splitlines()]
        versions.append("\n")
        # We need to insert the versions in reversed order
        versions.reverse()
        versions.append("    # FIXME: Added by `spack checksum`\n")
        version_line = None

        with open(filename, "r") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                # Black is drunk, so this is what it looks like for now
                # See https://github.com/psf/black/issues/2156 for more information
                if lines[i].startswith("    # FIXME: Added by `spack checksum`") or lines[
                    i
                ].startswith("    version("):
                    version_line = i
                    break

        if version_line is not None:
            for v in versions:
                lines.insert(version_line, v)

            with open(filename, "w") as f:
                f.writelines(lines)

            msg = "opening editor to verify"

            if not sys.stdout.isatty():
                msg = "please verify"

            tty.info(
                "Added {0} new versions to {1}, "
                "{2}.".format(len(versions) - 2, args.package, msg)
            )

            if sys.stdout.isatty():
                editor(filename)
        else:
            tty.warn("Could not add new versions to {0}.".format(args.package))
