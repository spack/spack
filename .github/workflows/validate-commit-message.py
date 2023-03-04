#!/usr/bin/env python

# requires: gitpython

import fileinput
import json
import logging
import os
import textwrap
from argparse import ArgumentParser

from git import Commit, Repo

EXISTING_PACKAGES = []

logger = logging.getLogger(__name__)
sh = logging.StreamHandler()
fmt = logging.Formatter("%(asctime)s %(message)s")
sh.setFormatter(fmt)
sh.setLevel(logging.DEBUG)
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)


def get_changed_packages(changed_files: list[str]) -> list[str]:
    """
    Return all packages changed by the commit
    """

    changed_packages = []
    changed_package_paths = [path for path in changed_files if "/packages/" in path]
    logger.debug("Changed package paths: %s", changed_package_paths)
    for package_path in changed_package_paths:
        path_components = package_path.split("/")
        changed_packages.append(path_components[path_components.index("packages") + 1])

    logger.debug("Changed packages: %s", changed_packages)
    return changed_packages


def get_unmentioned_packages(prefixes: list[str], changed_files: list[str]) -> list[str]:
    unmentioned_packages = []

    changed_packages = get_changed_packages(changed_files)

    for package in changed_packages:
        if package not in prefixes:
            unmentioned_packages.append(package)

    logger.debug("Packages changed but not mentioned: %s", unmentioned_packages)
    return unmentioned_packages


def one_package_mentioned(prefixes: list[str], changed_files: list[str]) -> list[str]:
    """Check whether at least one changed package is mentioned"""

    changed_packages = get_changed_packages(changed_files)
    return len([prefix for prefix in prefixes if prefix in changed_packages]) > 0


def collect_prefixes(message: str) -> list[str]:
    """
    Collect all prefixes in the commit message
    """
    prefixes = []

    for line in message.splitlines():
        if ":" in line:
            prefix = message.split(":")[0]
            prefix_items = [item.strip() for item in prefix.split(",")]
            prefixes.extend(prefix_items)

    logger.debug("Prefixes: %s", prefixes)
    return prefixes


def process_message(
    message: str,
    changed_files: list[str],
    docs_changed: bool,
    deploy_changed: bool,
    commit: Commit = None,
) -> str:
    """
    Process a message (PR title or commit message).
    If issues are found, return a message describing them.
    """
    logger.debug("Processing message: %s", message)
    prefixes = collect_prefixes(message)
    message = ""

    minimal_prefix_present = False
    if one_package_mentioned(prefixes, changed_files):
        logger.debug("At least one package was mentioned")
        minimal_prefix_present = True
    elif docs_changed and "docs" in prefixes:
        logger.debug("Docs were changed and mentioned")
        minimal_prefix_present = True
    elif deploy_changed and "deploy" in prefixes:
        logger.debug("Deploy was changed and mentioned")
        minimal_prefix_present = True

    if not minimal_prefix_present:
        unmentioned_packages = get_unmentioned_packages(prefixes, changed_files)
        if unmentioned_packages:
            message += textwrap.dedent(
                f"""\
                * The following packages were changed but not mentioned:
                  `{", ".join(unmentioned_packages)}:`
                  You can simply use the above list, \
                  then explain what you changed.
                  Alternatively, you can use one line per package \
                  to describe the change per package.
                  Please mention at least one package.
                """
            )

        if docs_changed and "docs" not in prefixes:
            message += textwrap.dedent(
                """\
                * Docs were changed but not mentioned.
                  Please use the `docs:` prefix to explain this change.
                """
            )

        if deploy_changed and "deploy" not in prefixes:
            message += textwrap.dedent(
                """\
                * Deploy files were changed but not mentioned.
                  Please use the `deploy:` prefix to explain this change.
                """
            )

    return message


def main(title: str, changed_files: list[str], commits: int) -> None:
    logger.info(
        "Setting fail state to make sure we catch any script failures- we'll clean up at the end"
    )
    with open(os.environ["GITHUB_OUTPUT"], "a") as fp:
        fp.write("script-failure=true\n")
    repo = Repo(".")

    logger.debug("Title: %s", title)
    logger.debug("Changed files: %s", changed_files)

    message_issues = []
    commit_issue = None
    title_issue = None
    warning = ""

    docs_changed = any("documentation" in changed_file for changed_file in changed_files)
    deploy_changed = any(
        changed_file.endswith("yml") or changed_file.endswith("yaml")
        for changed_file in changed_files
    )

    if commits > 1:
        title_issue = process_message(title, changed_files, docs_changed, deploy_changed)
    else:
        title_issue = process_message(title, changed_files, docs_changed, deploy_changed)

        commit = next(repo.iter_commits())
        logger.info(f"Checking commit: {commit.message} (parents: {commit.parents})")

        commit_issue = process_message(
            commit.message, changed_files, docs_changed, deploy_changed, commit
        )

    if title_issue:
        message_issues.append(title_issue)
        warning += textwrap.dedent(
            """\
            There are one or more issues with the title of this PR.
            """
        )

    if commit_issue:
        message_issues.append(commit_issue)
        quoted_commit_message = textwrap.indent(commit.message, prefix="  > ")

        warning += textwrap.dedent(
            f"""\
            There are one or more issues with the commit message of commit {commit.hexsha}.
            Commit message:

            {quoted_commit_message}
            """
        )

    if commit_issue or title_issue:
        if commits == 1:
            one_commit = "The commit message of your commit must be compliant as well."
        else:
            one_commit = ""
        warning += textwrap.dedent(
            f"""\
            Please satisfy at least one of the checks (one package, docs, or deploy).
            The PR title must be compliant. {one_commit}
            Issues:
            """
        )
        message_issues.insert(0, warning)
        with open("message_issues.txt", "w") as fp:
            fp.write("\n".join(message_issues))
        with open(os.environ["GITHUB_OUTPUT"], "a") as fp:
            fp.write("faulty-commits=true")

    with fileinput.FileInput(os.environ["GITHUB_OUTPUT"], inplace=True) as file:
        for line in file:
            print(line.replace("script-failure=true", "script-failure=false"))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--title", required=True, help="PR title")
    parser.add_argument(
        "--changed-files",
        required=True,
        help="JSON formatted list of files changed in PR",
    )
    parser.add_argument("--commits", required=True, help="Number of commits in the PR")

    args = parser.parse_args()

    for spack_repo in [
        "./var/spack/repos/builder.test",
        "./var/spack/repos/builtin",
        "./var/spack/repos/builtin.mock",
        "./var/spack/repos/tutorial",
        "./bluebrain/repo-bluebrain",
        "./bluebrain/repo-patches",
    ]:
        try:
            EXISTING_PACKAGES.extend(next(os.walk(f"{spack_repo}/packages"))[1])
        except StopIteration:
            logger.critical(f"No packages under {spack_repo}")
            pass

    main(args.title, json.loads(args.changed_files), int(args.commits))
