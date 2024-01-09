import os
import re

from llnl.util import tty
from llnl.util.filesystem import filter_file

import spack.repo
from spack.util.executable import which
from spack.util.naming import simplify_name

description = """Modify package recipes for use in CI pipelines.

This accepts zero or more expressions of the form PKG_{BRANCH,COMMIT,TAG}=VALUE
and uses them to modify package recipes in the current Spack tree.

If a branch or tag is given, this is immediately translated into a commit hash
and processing continues as if a commit had been given to start with. If the
optional --write-commit-file=FILE argument is given then FILE will contain the
results of this translation in the form of one PKG_COMMIT=HASH declaration per
line.

For each expression the upper case package name (PKG) is transformed into the
name of a Spack package, and the package preferences for that package are modified:
 - to require the given commit
 - set the given commit equivalent to the `develop` version

If PKG cannot be uniquely mapped to a Spack package, or if multiple expressions
are given for the same Spack package, an error code is returned.
"""
section = "extensions"
level = "short"


def setup_parser(subparser):
    scopes = spack.config.scopes()

    # User can only choose one
    subparser.add_argument(
        "--scope",
        choices=scopes,
        default="site",
        metavar=spack.config.SCOPES_METAVAR,
        help="configuration scope to read/modify",
    )

    subparser.add_argument(
        "--ignore-packages",
        nargs="*",
        type=str,
        default=[],
        help="PACKAGE specifications to ignore if passed as positional arguments.",
    )
    subparser.add_argument(
        "--write-commit-file",
        default=None,
        type=str,
        help="File to write {PACKAGE}_COMMIT=1234 values to.",
    )
    subparser.add_argument(
        "modifications", nargs="*", type=str, help="PACKAGE_{BRANCH,COMMIT,TAG}=foo values"
    )


def configure_pipeline(parser, args):
    # Parse all of our inputs before trying to modify any recipes.
    modifications = {}
    packages_to_ignore = set(args.ignore_packages)
    mod_pattern = re.compile("^([^=]+)_(BRANCH|COMMIT|TAG)=(.*)$", re.IGNORECASE)
    for mod_str in args.modifications:
        match = mod_pattern.match(mod_str)
        if not match:
            raise Exception("Could not parse: {}".format(mod_str))
        package_name = match.group(1)
        ref_type = match.group(2).lower()
        val = match.group(3)
        # Handle --ignore-packges arguments
        if package_name in packages_to_ignore:
            tty.info("{}: ignoring {}".format(package_name, mod_str))
            continue
        # Try and transform the input name, which is probably all upper case
        # and may contain underscores, into a Spack-style name that is all
        # lower case and contains hyphens.
        spack_package_name = simplify_name(package_name)
        # Check if this package exists
        try:
            spack.repo.PATH.get_pkg_class(spack_package_name)
        except spack.repo.UnknownPackageError:
            raise Exception(
                "Could not find a Spack package corresponding to {}, tried {}".format(
                    package_name, spack_package_name
                )
            )
        if spack_package_name in modifications:
            raise Exception(
                "Parsed multiple modifications for Spack package {} from: {}".format(
                    spack_package_name, " ".join(args.modifications)
                )
            )
        modifications[spack_package_name] = {
            "bash_name": package_name,
            "ref_type": ref_type,
            "ref": val,
        }

    # Translate any branches or tags into commit hashes and then use those
    # consistently. This guarantees different jobs in a pipeline all get the
    # same commit, and means we can handle provenance information (what did
    # @develop mean) in one place.
    git = which("git")
    if not git:
        raise Exception("Git is required")
    for spack_package_name, info in modifications.items():
        if info["ref_type"] == "commit":
            info["commit"] = info["ref"]
        else:
            if info["ref_type"] == "branch":
                remote_ref = "refs/heads/" + info["ref"]
            else:
                assert info["ref_type"] == "tag"
                remote_ref = "refs/tags/" + info["ref"]
            spack_package = spack.repo.PATH.get_pkg_class(spack_package_name)
            remote_refs = git("ls-remote", spack_package.git, remote_ref, output=str).splitlines()
            assert len(remote_refs) < 2
            if len(remote_refs) == 0:
                raise Exception(
                    "Could not find {} {} on remote {} (tried {})".format(
                        info["ref_type"], info["ref"], spack_package.git, remote_ref
                    )
                )
            commit, ref_check = remote_refs[0].split()
            assert remote_ref == ref_check
            tty.info(
                "{}: resolved {} {} to {}".format(
                    spack_package_name, info["ref_type"], info["ref"], commit
                )
            )
            info["commit"] = commit

    if args.write_commit_file is not None:
        with open(args.write_commit_file, "w") as ofile:
            for spack_package_name, info in modifications.items():
                ofile.write("{}_COMMIT={}\n".format(info["bash_name"], info["commit"]))

    # Now modify the Spack recipes of the given packages
    for spack_package_name, info in modifications.items():
        cfg = f"packages:{spack_package_name}:require: '@git.{info['commit']}=develop'"
        tty.info(f"adding config: {cfg}")
        spack.config.add(cfg, args.scope)
