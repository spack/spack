#!/usr/bin/env spack-python
import re
import sys
import tempfile
from typing import Dict

import llnl.util.filesystem as fs
from llnl.util import tty
from llnl.util.filesystem import working_dir

import spack.paths
import spack.repo
import spack.util.git
from spack.ci import get_added_versions
from spack.util.executable import ProcessError
from spack.version import StandardVersion

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


def validate_standard_version(pkg, version: StandardVersion) -> bool:
    """Get and test the checksum of a package version based on a tarball.

    Args:
      pkg (Package): Spack package for which to validate a version checksum
      version (StandardVersion): version of the package to validate

    Returns:
      bool: result of the validation. True is valid and false is failed.
    """
    sha = get_standard_version_checksum(pkg, version)
    if sha != pkg.versions[version]["sha256"]:
        tty.error(
            f"Invalid checksum found {pkg.name}@{version}\n"
            f"    [package.py] {pkg.versions[version]['sha256']}\n"
            f"    [Downloaded] {sha}"
        )
        return False

    tty.info(f"Validated {pkg.name}@{version} --> {sha}")
    return True


def validate_git_version(pkg, version: StandardVersion) -> bool:
    """Get and test the commit and tag of a package version based on a git repository.

    Args:
      pkg (Package): Spack package for which to validate a version commit / tag
      version (StandardVersion): version of the package to validate

    Returns:
      bool: result of the validation. True is valid and false is failed.
    """
    known_commit = pkg.versions[version]["commit"]
    git = spack.util.git.git(required=True)

    with tempfile.TemporaryDirectory() as tmpdirpath:
        # Test if repository can be cloned.
        try:
            git("clone", pkg.git, tmpdirpath, output=str, error=str)
        except ProcessError as exp:
            tty.error(f"Unable to clone git repository for {pkg.name}@{version}", exp)

        with working_dir(tmpdirpath):
            # Test if the specified commit is in the repository.
            # If the commit is located in the repository the command will return 0 and
            # print the word "commit" else it will fail with a lookup error
            try:
                git("cat-file", "-t", known_commit, output=str, error=str)

            except ProcessError as exp:
                tty.error(
                    f"Invalid commit for {pkg.name}@{version}\n"
                    f"    {known_commit} could not be located in git repository."
                )
                return False

            # Test if the specified tag matches the commit in the package.py
            # We retrieve the commit associated with a tag and compare it to the
            # commit that is located in the package.py file.
            if "tag" in pkg.versions[version]:
                tag = pkg.versions[version]["tag"]
                found_commit = git("rev-list", "-n", "1", tag, output=str).strip()
                if found_commit != known_commit:
                    tty.error(
                        f"Mismatched tag <--> commit found for {pkg.name}@{version}\n"
                        f"    [package.py] {known_commit}\n"
                        f"    [Downloaded] {found_commit}"
                    )
                    return False

    # If we have downloaded the repository, found the commit, and compared
    # the tag (if specified) we can conclude that the version is pointing
    # at what we would expect.
    tty.info(f"Validated {pkg.name}@{version} --> {known_commit}")
    return True


def main():
    with fs.working_dir(spack.paths.prefix):
        # We use HEAD^1 explicitly on the merge commit created by
        # GitHub Actions. However HEAD~1 is a safer default for the helper function.
        files = spack.util.git.get_modified_files(from_ref="HEAD^1")

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
            if "sha256" in pkg.versions[version]:
                checksums_version_dict[pkg.versions[version]["sha256"]] = version

            elif "commit" in pkg.versions[version]:
                checksums_version_dict[pkg.versions[version]["commit"]] = version

            elif not version.isdevelop():
                tty.error(f"{pkg_name}@{version} does not define a sha256 or commit.")
                failed_checksum = True

        with fs.working_dir(spack.paths.prefix):
            added_versions = get_added_versions(checksums_version_dict, path, from_ref="HEAD^1")

        print(added_versions)

        for version in added_versions:
            # Verify package versions coming from tarballs
            if "sha256" in pkg.versions[version]:
                failed_checksum = not validate_standard_version(pkg, version)

            if "commit" in pkg.versions[version]:
                failed_checksum = not validate_git_version(pkg, version)

    if failed_checksum:
        sys.exit(1)


if __name__ == "__main__":
    main()
