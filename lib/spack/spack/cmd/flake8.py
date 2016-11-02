##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import re
import os
import sys
import shutil
import tempfile
import argparse

from llnl.util.filesystem import *

import spack
from spack.util.executable import *

description = "Runs source code style checks on Spack. Requires flake8."

changed_files_path = os.path.join(spack.share_path, 'qa', 'changed_files')
changed_files = Executable(changed_files_path)
flake8 = None

#
# This is a dict that maps:
# filename pattern ->
#    a flake8 exemption code ->
#       list of patterns, for which matching lines should have codes applied.
#
exemptions = {
    # exemptions applied only to package.py files.
    r'package.py$': {
        # Exempt lines with urls and descriptions from overlong line errors.
        501: [r'^\s*homepage\s*=',
              r'^\s*url\s*=',
              r'^\s*version\(.*\)',
              r'^\s*variant\(.*\)',
              r'^\s*depends_on\(.*\)',
              r'^\s*extends\(.*\)'],
        # Exempt '@when' decorated functions from redefinition errors.
        811: [r'^\s*\@when\(.*\)'],
    },

    # exemptions applied to all files.
    r'.py$': {
        # Exempt lines with URLs from overlong line errors.
        501: [r'^(https?|file)\:']
    },
}

# compile all regular expressions.
exemptions = dict((re.compile(file_pattern),
                   dict((code, [re.compile(p) for p in patterns])
                        for code, patterns in error_dict.items()))
                  for file_pattern, error_dict in exemptions.items())


def filter_file(source, dest):
    """Filter a single file through all the patterns in exemptions."""
    with open(source) as infile:
        parent = os.path.dirname(dest)
        mkdirp(parent)

        with open(dest, 'w') as outfile:
            for file_pattern, errors in exemptions.items():
                if not file_pattern.search(source):
                    continue

                for line in infile:
                    line = line.rstrip()

                    for code, patterns in errors.items():
                        for pattern in patterns:
                            if pattern.search(line):
                                line += ("  # NOQA: ignore=%d" % code)
                                break
                    outfile.write(line + '\n')


def setup_parser(subparser):
    subparser.add_argument(
        '-k', '--keep-temp', action='store_true',
        help="Do not delete temporary directory where flake8 runs. "
             "Use for debugging, to see filtered files.")
    subparser.add_argument(
        '-r', '--root-relative', action='store_true', default=False,
        help="print root-relative paths (default is cwd-relative)")
    subparser.add_argument(
        'files', nargs=argparse.REMAINDER, help="specific files to check")


def flake8(parser, args):
    # Just use this to check for flake8 -- we actually execute it with Popen.
    global flake8
    flake8 = which('flake8', required=True)

    temp = tempfile.mkdtemp()
    try:
        file_list = args.files
        if file_list:
            def prefix_relative(path):
                return os.path.relpath(
                    os.path.abspath(os.path.realpath(path)), spack.prefix)

            file_list = [prefix_relative(p) for p in file_list]

        with working_dir(spack.prefix):
            if not file_list:
                file_list = changed_files('*.py', output=str)
                file_list = [x for x in file_list.split('\n') if x]

            shutil.copy('.flake8', os.path.join(temp, '.flake8'))

        print '======================================================='
        print 'flake8: running flake8 code checks on spack.'
        print
        print 'Modified files:'
        for filename in file_list:
            print "  %s" % filename.strip()
        print('=======================================================')

        # filter files into a temporary directory with exemptions added.
        for filename in file_list:
            src_path = os.path.join(spack.prefix, filename)
            dest_path = os.path.join(temp, filename)
            filter_file(src_path, dest_path)

        # run flake8 on the temporary tree.
        with working_dir(temp):
            output = flake8('--format', 'pylint', *file_list,
                            fail_on_error=False, output=str)

        if args.root_relative:
            # print results relative to repo root.
            print output
        else:
            # print results relative to current working directory
            def cwd_relative(path):
                return '%s: [' % os.path.relpath(
                    os.path.join(spack.prefix, path.group(1)), os.getcwd())

            for line in output.split('\n'):
                print re.sub(r'^(.*): \[', cwd_relative, line)

        if flake8.returncode != 0:
            print "Flake8 found errors."
            sys.exit(1)
        else:
            print "Flake8 checks were clean."

    finally:
        if args.keep_temp:
            print "temporary files are in ", temp
        else:
            shutil.rmtree(temp, ignore_errors=True)
