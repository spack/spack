#!/usr/bin/env python
#
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Maintainer review action.

This action checks which packages have changed in a PR, and adds their
maintainers to the pull request for review.
"""

import json
import os
import re
import subprocess

from github import Github


def spack(*args):
    """Run the spack executable with arguments, and return the output split.

    This does just enough to run `spack pkg` and `spack maintainers`, the
    two commands used by this action.
    """
    github_workspace = os.environ['GITHUB_WORKSPACE']
    spack = os.path.join(github_workspace, 'bin', 'spack')
    output = subprocess.check_output([spack] + list(args))
    split = re.split(r'\s*', output.decode('utf-8').strip())
    return [s for s in split if s]


def main():
    # get these first so that we'll fail early
    token = os.environ['GITHUB_TOKEN']
    event_path = os.environ['GITHUB_EVENT_PATH']

    with open(event_path) as file:
        data = json.load(file)

    # make sure it's a pull_request event
    assert 'pull_request' in data

    # only request reviews on open, edit, or reopen
    action = data['action']
    if action not in ('opened', 'edited', 'reopened'):
        return

    # get data from the event payload
    pr_data             = data['pull_request']
    base_branch_name    = pr_data['base']['ref']
    full_repo_name      = pr_data['base']['repo']['full_name']
    pr_number           = pr_data['number']
    requested_reviewers = pr_data['requested_reviewers']
    author              = pr_data['user']['login']

    # get a list of packages that this PR modified
    changed_pkgs = spack(
        'pkg', 'changed', '--type', 'ac', '%s...' % base_branch_name)

    # get maintainers for all modified packages
    maintainers = set()
    for pkg in changed_pkgs:
        pkg_maintainers = set(spack('maintainers', pkg))
        maintainers |= pkg_maintainers

    # remove any maintainers who are already on the PR, and the author,
    # as you can't review your own PR)
    maintainers -= set(requested_reviewers)
    maintainers -= set([author])

    if not maintainers:
        return

    # request reviews from each maintainer
    gh = Github(token)
    repo = gh.get_repo(full_repo_name)
    pr = repo.get_pull(pr_number)
    pr.create_review_request(list(maintainers))


if __name__ == "__main__":
    main()
