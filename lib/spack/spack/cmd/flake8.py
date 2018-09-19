##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from __future__ import print_function

import re
import os
import sys
import shutil
import tempfile
import argparse

from llnl.util.filesystem import working_dir, mkdirp

import spack.paths
from spack.util.executable import which


description = "runs source code style checks on Spack. requires flake8"
section = "developer"
level = "long"


def is_package(f):
    """Whether flake8 should consider a file as a core file or a package.

    We run flake8 with different exceptions for the core and for
    packages, since we allow `from spack import *` and poking globals
    into packages.
    """
    return f.startswith('var/spack/repos/') or 'docs/tutorial/examples' in f


#: List of directories to exclude from checks.
exclude_directories = [spack.paths.external_path]


#: This is a dict that maps:
#:  filename pattern ->
#:     flake8 exemption code ->
#:        list of patterns, for which matching lines should have codes applied.
#:
#: For each file, if the filename pattern matches, we'll add per-line
#: exemptions if any patterns in the sub-dict match.
pattern_exemptions = {
    # exemptions applied only to package.py files.
    r'package.py$': {
        # Allow 'from spack import *' in packages, but no other wildcards
        'F403': [
            r'^from spack import \*$'
        ],
        # Exempt lines with urls and descriptions from overlong line errors.
        'E501': [
            r'^\s*homepage\s*=',
            r'^\s*url\s*=',
            r'^\s*git\s*=',
            r'^\s*svn\s*=',
            r'^\s*hg\s*=',
            r'^\s*list_url\s*=',
            r'^\s*version\(',
            r'^\s*variant\(',
            r'^\s*provides\(',
            r'^\s*extends\(',
            r'^\s*depends_on\(',
            r'^\s*conflicts\(',
            r'^\s*resource\(',
            r'^\s*patch\(',
        ],
        # Exempt '@when' decorated functions from redefinition errors.
        'F811': [
            r'^\s*@when\(.*\)',
        ],
    },

    # exemptions applied to all files.
    r'.py$': {
        'E501': [
            r'(https?|ftp|file)\:',        # URLs
            r'([\'"])[0-9a-fA-F]{32,}\1',  # long hex checksums
        ]
    },
}

# compile all regular expressions.
pattern_exemptions = dict(
    (re.compile(file_pattern),
     dict((code, [re.compile(p) for p in patterns])
          for code, patterns in error_dict.items()))
    for file_pattern, error_dict in pattern_exemptions.items())


def changed_files(args):
    """Get list of changed files in the Spack repository."""

    git = which('git', required=True)

    range = "{0}...".format(args.base)

    git_args = [
        # Add changed files committed since branching off of develop
        ['diff', '--name-only', '--diff-filter=ACMR', range],
        # Add changed files that have been staged but not yet committed
        ['diff', '--name-only', '--diff-filter=ACMR', '--cached'],
        # Add changed files that are unstaged
        ['diff', '--name-only', '--diff-filter=ACMR'],
    ]

    # Add new files that are untracked
    if args.untracked:
        git_args.append(['ls-files', '--exclude-standard', '--other'])

    # add everything if the user asked for it
    if args.all:
        git_args.append(['ls-files', '--exclude-standard'])

    excludes = [os.path.realpath(f) for f in exclude_directories]
    changed = set()

    for arg_list in git_args:
        files = git(*arg_list, output=str).split('\n')

        for f in files:
            # Ignore non-Python files
            if not f.endswith('.py'):
                continue

            # Ignore files in the exclude locations
            if any(os.path.realpath(f).startswith(e) for e in excludes):
                continue

            changed.add(f)

    return sorted(changed)


def add_pattern_exemptions(line, codes):
    """Add a flake8 exemption to a line."""
    if line.startswith('#'):
        return line

    line = line.rstrip('\n')

    # Line is already ignored
    if line.endswith('# noqa'):
        return line + '\n'

    orig_len = len(line)
    exemptions = ','.join(sorted(set(codes)))

    # append exemption to line
    if '# noqa: ' in line:
        line += ',{0}'.format(exemptions)
    elif line:  # ignore noqa on empty lines
        line += '  # noqa: {0}'.format(exemptions)

    # if THIS made the line too long, add an exemption for that
    if len(line) > 79 and orig_len <= 79:
        line += ',E501'

    return line + '\n'


def filter_file(source, dest, output=False):
    """Filter a single file through all the patterns in pattern_exemptions."""
    with open(source) as infile:
        parent = os.path.dirname(dest)
        mkdirp(parent)

        with open(dest, 'w') as outfile:
            for line in infile:
                line_errors = []

                # pattern exemptions
                for file_pattern, errors in pattern_exemptions.items():
                    if not file_pattern.search(source):
                        continue

                    for code, patterns in errors.items():
                        for pattern in patterns:
                            if pattern.search(line):
                                line_errors.append(code)
                                break

                if line_errors:
                    line = add_pattern_exemptions(line, line_errors)

                outfile.write(line)
                if output:
                    sys.stdout.write(line)


def setup_parser(subparser):
    subparser.add_argument(
        '-b', '--base', action='store', default='develop',
        help="select base branch for collecting list of modified files")
    subparser.add_argument(
        '-k', '--keep-temp', action='store_true',
        help="do not delete temporary directory where flake8 runs. "
             "use for debugging, to see filtered files")
    subparser.add_argument(
        '-a', '--all', action='store_true',
        help="check all files, not just changed files")
    subparser.add_argument(
        '-o', '--output', action='store_true',
        help="send filtered files to stdout as well as temp files")
    subparser.add_argument(
        '-r', '--root-relative', action='store_true', default=False,
        help="print root-relative paths (default: cwd-relative)")
    subparser.add_argument(
        '-U', '--no-untracked', dest='untracked', action='store_false',
        default=True, help="exclude untracked files from checks")
    subparser.add_argument(
        'files', nargs=argparse.REMAINDER, help="specific files to check")


def flake8(parser, args):
    flake8 = which('flake8', required=True)

    temp = tempfile.mkdtemp()
    try:
        file_list = args.files
        if file_list:
            def prefix_relative(path):
                return os.path.relpath(
                    os.path.abspath(os.path.realpath(path)),
                    spack.paths.prefix)

            file_list = [prefix_relative(p) for p in file_list]

        with working_dir(spack.paths.prefix):
            if not file_list:
                file_list = changed_files(args)

        print('=======================================================')
        print('flake8: running flake8 code checks on spack.')
        print()
        print('Modified files:')
        for filename in file_list:
            print('  {0}'.format(filename.strip()))
        print('=======================================================')

        # filter files into a temporary directory with exemptions added.
        for filename in file_list:
            src_path = os.path.join(spack.paths.prefix, filename)
            dest_path = os.path.join(temp, filename)
            filter_file(src_path, dest_path, args.output)

        # run flake8 on the temporary tree, once for core, once for pkgs
        package_file_list = [f for f in file_list if is_package(f)]
        file_list         = [f for f in file_list if not is_package(f)]

        returncode = 0
        with working_dir(temp):
            output = ''
            if file_list:
                output += flake8(
                    '--format', 'pylint',
                    '--config=%s' % os.path.join(spack.paths.prefix,
                                                 '.flake8'),
                    *file_list, fail_on_error=False, output=str)
                returncode |= flake8.returncode
            if package_file_list:
                output += flake8(
                    '--format', 'pylint',
                    '--config=%s' % os.path.join(spack.paths.prefix,
                                                 '.flake8_packages'),
                    *package_file_list, fail_on_error=False, output=str)
                returncode |= flake8.returncode

        if args.root_relative:
            # print results relative to repo root.
            print(output)
        else:
            # print results relative to current working directory
            def cwd_relative(path):
                return '{0}: ['.format(os.path.relpath(
                    os.path.join(
                        spack.paths.prefix, path.group(1)), os.getcwd()))

            for line in output.split('\n'):
                print(re.sub(r'^(.*): \[', cwd_relative, line))

        if returncode != 0:
            print('Flake8 found errors.')
            sys.exit(1)
        else:
            print('Flake8 checks were clean.')

    finally:
        if args.keep_temp:
            print('Temporary files are in: ', temp)
        else:
            shutil.rmtree(temp, ignore_errors=True)
