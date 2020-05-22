#!/usr/bin/env python3
#
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Maintainer action.

This action checks which packages have changed in a PR, and checks
whether or not these packages have maintainers.
"""

import argparse
import os
import pathlib
import subprocess


def spack(*args):
    """Run the spack executable with arguments, and return the output split.
    """
    github_workspace = os.environ['GITHUB_WORKSPACE']
    spack = os.path.join(github_workspace, 'bin', 'spack')
    output = subprocess.run([spack] + list(args), stdout=subprocess.PIPE)
    return output.stdout.decode('utf-8').split()


def main(author, changes):
    """Main action method.

    Parameters:
        author (str): the GitHub login of the PR author
        changes (list): the files changed in this PR
    """
    # Find a set of modified packages
    changed_pkgs = set()
    for filename in changes:
        if filename.startswith('var/spack/repos/builtin/packages/'):
            filename = pathlib.Path(filename)
            pkg = filename.parts[5]
            changed_pkgs.add(pkg)

    # Get maintainers for all modified packages
    packages_with_maintainers = []
    packages_without_maintainers = []
    maintainers = set()
    for pkg in changed_pkgs:
        pkg_maintainers = set(spack('maintainers', pkg))

        if not pkg_maintainers:
            packages_without_maintainers.append(pkg)

        # No need to ask the author to review their own PR
        pkg_maintainers.discard(author)

        if pkg_maintainers:
            packages_with_maintainers.append(pkg)
            maintainers |= pkg_maintainers

    # Return outputs so that later GitHub actions can access them
    print('::set-output name=packages-with-maintainers::{}'.format(
        '\n* '.join(packages_with_maintainers)))
    print('::set-output name=packages-without-maintainers::{}'.format(
        '\n* '.join(packages_without_maintainers)))
    print('::set-output name=maintainers::{}'.format(' @'.join(maintainers)))


if __name__ == '__main__':
    # Set up parser
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('author', help='GitHub username of PR author')
    parser.add_argument('changes',
                        help='Comma-separated list of changed files')

    # Parse supplied arguments
    args = parser.parse_args()

    main(args.author, args.changes.split(','))
