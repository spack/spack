# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

from llnl.util import tty
from llnl.util.tty.colify import colify

import spack.repo
import spack.spec
import spack.store
from spack.installer import InstallError, PackageInstaller
from spack.package_file import add_versions_to_package
from spack.util.format import get_version_lines
from spack.version import infinity_versions

description = "discover and test new versions of a package"
section = "packaging"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        "--mark",
        default="implicit",
        choices=["implicit", "explicit"],
        help="mark pkgs after installation to keep/cleanup",
    )
    subparser.add_argument(
        "--test",
        "-t",
        default=None,
        choices=["root", "all"],
        help="build pkgs with tests to validate",
    )
    subparser.add_argument("pkgs", nargs=argparse.REMAINDER, help="packages to update")


def scout(parser, args):
    for pkg_name in args.pkgs:
        tty.info(f"Checking for updates to {pkg_name}")
        pkg_cls = spack.repo.PATH.get_pkg_class(pkg_name)
        pkg = pkg_cls(spack.spec.Spec(pkg_name))

        # retrieve a list of the known package versions
        safe_versions = sorted(pkg.versions, reverse=True)
        if len(safe_versions) <= 0:
            tty.warn(f"No previously checksummed versions for {pkg_name}")

        # retrieve a list of new unchecksummed versions
        fetched_versions = pkg.fetch_remote_versions()
        if len(fetched_versions) <= 0:
            tty.die(f"Unable to find any remote versions for {pkg_name}")

        # filter out any infinite versions such as git branches
        numeric_safe_versions = set(
            filter(lambda v: str(v) not in infinity_versions, safe_versions)
        )

        # get the highest known and remote version
        highest_safe_version = max(numeric_safe_versions)
        highest_fetched_version = max(fetched_versions)

        # exit if no newer versions have been released
        if highest_fetched_version <= highest_safe_version:
            tty.info(f"No new version found for {pkg_name}")
            continue

        # create url_dict to map the newer remote version to a url
        url_dict = {highest_fetched_version: fetched_versions[highest_fetched_version]}

        # checksum the newer remote version
        version_hashes = spack.stage.get_checksums_for_versions(url_dict, pkg.name)

        # take a backup of a package's class file
        filename = spack.repo.PATH.filename_for_package_name(pkg.name)
        with open(filename, "r+") as f:
            file_backup = f.read()

        # render the version lines to add to the package file
        version_lines = get_version_lines(version_hashes, url_dict)
        added_lines = add_versions_to_package(pkg, version_lines)

        # ensure that a newer version was added to the package
        if added_lines < 1:
            tty.warn(f"Could not add new version to {pkg_name}")
            continue

        # create spec of newer version to build
        spec = spack.spec.Spec(f"{pkg_name}@={highest_fetched_version}")
        spec.concretize()

        # attempt to build the updated package
        try:
            install_kwargs = {}
            if args.test is not None:
                install_kwargs["test"] = [pkg_name]

            builder = PackageInstaller([(spec.package, install_kwargs)])
            builder.install()

            # mark packages as implicit by default to cleanup with "spack gc"
            spack.store.STORE.db.update_explicit(spec, explicit=(args.mark == "explicit"))

        # overwrite modified file with backup on failed build
        except InstallError:
            with open(filename, "w") as f:
                f.write(file_backup)

            tty.warn(f"Could not build {pkg_name}@{highest_fetched_version}")
            continue

        tty.msg(f"Sucessfully built {pkg_name}@{highest_fetched_version} and added version to")
        colify([filename], indent=4)
