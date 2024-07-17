#!/usr/bin/env spack-python
import re
from typing import Dict, List, Union

import llnl.util.filesystem as fs
from llnl.util import tty

import spack.paths
import spack.repo
import spack.util.git
from spack.version import GitVersion, StandardVersion

BUILTIN = re.compile(r"var\/spack\/repos\/builtin\/packages\/([^\/]+)\/package\.py")


def get_modified_files(from_ref: str = "HEAD~1", to_ref: str = "HEAD") -> List[str]:
    """Get a list of files modified between `from_ref` and `to_ref`

    Args:
       from_ref (str): oldest git ref, defaults to `HEAD~1`
       to_ref (str): newer git ref, defaults to `HEAD`

    Returns:
      files (list): list of file paths
    """
    git = spack.util.git.git(required=True)

    with fs.working_dir(spack.paths.prefix):
        stdout = git("diff", "--name-only", from_ref, to_ref, output=str)

    return stdout.split()


def get_added_versions(
    checksums_version_dict: Dict[str, Union[StandardVersion, GitVersion]],
    path: str,
    from_ref: str = "HEAD~1",
    to_ref: str = "HEAD",
) -> List[Union[StandardVersion, GitVersion]]:
    """Get a list of the versions added between `from_ref` and `to_ref`.

    Args:
       checksums_version_dict (Dict): all package versions mapped to known checksums.
       path (str): path to the package.py
       from_ref (str): oldest git ref, defaults to `HEAD~1`
       to_ref (str): newer git ref, defaults to `HEAD`

    Returns:
       versions_list (List): list of versions added between refs
    """
    git = spack.util.git.git(required=True)

    # Gather git diff
    diff_lines = git("diff", from_ref, to_ref, "--", path, output=str).split("\n")

    # Store added and removed versions
    added_checksums = set()
    removed_checksums = set()

    # Scrape diff for modified versions
    for checksum in checksums_version_dict.keys():
        for line in diff_lines:
            if checksum in line:
                if line.startswith("+"):
                    added_checksums.add(checksum)
                if line.startswith("-"):
                    removed_checksums.add(checksum)

    return [checksums_version_dict[c] for c in added_checksums - removed_checksums]


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
