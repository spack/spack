#!/usr/bin/env spack-python
import re
from typing import Dict

import llnl.util.filesystem as fs
from llnl.util import tty

import spack.paths
import spack.repo
from spack.util.git import get_added_versions, get_modified_files
from spack.version import GitVersion, StandardVersion

BUILTIN = re.compile(r"var\/spack\/repos\/builtin\/packages\/([^\/]+)\/package\.py")


def get_standard_version_checksum(pkg, version: StandardVersion) -> str:
    """Get a checksum for a Spack StandardVersion.

    Args:
       pkg (Package): Spack package for which to get a version checksum
       version (StandardVersion): version in package to get checksum

    Returns:
      checksum (str): sha256 checksum of version tarball
    """
    url = pkg.find_valid_url_for_version(version)
    url_dict: Dict[StandardVersion, str] = {version: url}

    version_hashes = spack.stage.get_checksums_for_versions(
        url_dict, pkg.name, fetch_options=pkg.fetch_options
    )

    return version_hashes[version]


def main():
    with fs.working_dir(spack.paths.prefix):
        files = get_modified_files()

    pkgs = [(m.group(1), p) for p in files for m in [BUILTIN.search(p)] if m]

    failed_checksum = False
    for pkg_name, path in pkgs:
        # Get the package we're going to generate checksums for
        spec = spack.spec.Spec(pkg_name)
        pkg = spack.repo.PATH.get_pkg_class(spec.name)(spec)

        # Skip checking manual download packages and trust the maintainers
        if pkg.manual_download:
            continue

        # Store versions checksums / commits for future loop
        checksums_version_dict = {}
        for version in pkg.versions:
            if isinstance(version, StandardVersion):
                if "sha256" in pkg.versions[version]:
                    checksums_version_dict[pkg.versions[version]["sha256"]] = version
                else:
                    tty.die(
                        f"{pkg_name}@{version} does not define a sha256 and is not a git version."
                    )

        with fs.working_dir(spack.paths.prefix):
            added_versions = get_added_versions(checksums_version_dict, path)

        for version in added_versions:
            # Verify package versions coming from tarballs
            if isinstance(version, StandardVersion):
                sha = get_standard_version_checksum(pkg, version)
                if sha == pkg.versions[version]["sha256"]:
                    tty.info(f"Validated {pkg_name}@{version} --> {sha}")
                else:
                    failed_checksum = True
                    tty.error(
                        f"Invalid checksum found {pkg_name}@{version}\n"
                        f"    [package.py] {pkg.versions[version]['sha256']}\n"
                        f"    [Downloaded] {sha}"
                    )

            # TODO: Verify package versions coming from git
            elif isinstance(version, GitVersion):
                pass

    if failed_checksum:
        tty.die("Invalid checksums found.")


if __name__ == "__main__":
    main()
