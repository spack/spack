# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Check that Spack complies with minimum supported python versions.

We ensure that all Spack files work with Python2 >= 2.6 and Python3 >= 3.0.

We'd like to drop 2.6 support at some point, but there are still many HPC
systems that ship with RHEL6/CentOS 6, which have Python 2.6 as the
default version.  Once those go away, we can likely drop 2.6 and increase
the minimum supported Python 3 version, as well.
"""
from __future__ import print_function

import os
import sys
import re

import pytest

import llnl.util.tty as tty

import spack.paths
from spack.paths import lib_path as spack_lib_path


#
# This test uses pyqver, by Greg Hewgill, which is a dual-source module.
# That means we need to do different checks depending on whether we're
# running Python 2 or Python 3.
#
if sys.version_info[0] < 3:
    import pyqver2 as pyqver
    spack_min_supported = (2, 6)

    # Exclude Python 3 versions of dual-source modules when using Python 2
    exclude_paths = [
        # Jinja 2 has some 'async def' functions that are not treated correctly
        # by pyqver.py
        os.path.join(spack_lib_path, 'external', 'jinja2', 'asyncfilters.py'),
        os.path.join(spack_lib_path, 'external', 'jinja2', 'asyncsupport.py'),
        os.path.join(spack_lib_path, 'external', 'yaml', 'lib3'),
        os.path.join(spack_lib_path, 'external', 'pyqver3.py'),
        # Uses importlib
        os.path.join(spack_lib_path, 'spack', 'test', 'schema.py')
    ]

else:
    import pyqver3 as pyqver
    spack_min_supported = (3, 0)

    # Exclude Python 2 versions of dual-source modules when using Python 3
    exclude_paths = [
        # Jinja 2 has some 'async def' functions that are not treated correctly
        # by pyqver.py
        os.path.join(spack_lib_path, 'external', 'jinja2', 'asyncfilters.py'),
        os.path.join(spack_lib_path, 'external', 'jinja2', 'asyncsupport.py'),
        os.path.join(spack_lib_path, 'external', 'yaml', 'lib'),
        os.path.join(spack_lib_path, 'external', 'pyqver2.py'),
        # Uses importlib
        os.path.join(spack_lib_path, 'spack', 'test', 'schema.py')
    ]


def pyfiles(search_paths, exclude=()):
    """Generator that yields all the python files in the search paths.

    Args:
        search_paths (list of str): list of paths to search for python files
        exclude (list of str): file paths to exclude from search

    Yields:
        python files in the search path.
    """
    # first file is the spack script.
    yield spack.paths.spack_script

    # Iterate through the whole spack source tree.
    for path in search_paths:
        for root, dirnames, filenames in os.walk(path):
            for filename in filenames:
                realpath = os.path.realpath(os.path.join(root, filename))
                if any(realpath.startswith(p) for p in exclude):
                    continue

                if re.match(r'^[^.#].*\.py$', filename):
                    yield os.path.join(root, filename)


def check_python_versions(files):
    """Check that a set of Python files works with supported Ptyhon versions"""
    # This is a dict dict mapping:
    #   version -> filename -> reasons
    #
    # Reasons are tuples of (lineno, string), where the string is the
    # cause for a version incompatibility.
    all_issues = {}

    # Parse files and run pyqver on each file.
    for path in files:
        with open(path) as pyfile:
            full_text = pyfile.read()
        versions = pyqver.get_versions(full_text, path)

        for ver, reasons in versions.items():
            if ver <= spack_min_supported:
                continue

            # Record issues. Mark exceptions with '# nopyqver' comment
            for lineno, cause in reasons:
                lines = full_text.split('\n')
                if not re.search(r'#\s*nopyqver\s*$', lines[lineno - 1]):
                    all_issues.setdefault(ver, {})[path] = reasons

    # Print a message if there are are issues
    if all_issues:
        tty.msg("Spack must remain compatible with Python version %d.%d"
                % spack_min_supported)

    # Print out a table showing which files/linenos require which
    # python version, and a string describing why.
    for v in sorted(all_issues.keys(), reverse=True):
        messages = []
        for path in sorted(all_issues[v].keys()):
            short_path = path
            if path.startswith(spack.paths.prefix):
                short_path = path[len(spack.paths.prefix):]

            reasons = [r for r in set(all_issues[v][path]) if r]
            for lineno, cause in reasons:
                file_line = "%s:%s" % (short_path.lstrip('/'), lineno)
                messages.append((file_line, cause))

        print()
        tty.msg("These files require version %d.%d:" % v)
        maxlen = max(len(f) for f, prob in messages)
        fmt = "%%-%ds%%s" % (maxlen + 3)
        print(fmt % ('File', 'Reason'))
        print(fmt % ('-' * (maxlen), '-' * 20))
        for msg in messages:
            print(fmt % msg)

    # Fail this test if there were issues.
    assert not all_issues


@pytest.mark.maybeslow
def test_core_module_compatibility():
    """Test that all core spack modules work with supported Python versions."""
    check_python_versions(
        pyfiles([spack_lib_path], exclude=exclude_paths))


@pytest.mark.maybeslow
def test_package_module_compatibility():
    """Test that all spack packages work with supported Python versions."""
    check_python_versions(pyfiles([spack.paths.packages_path]))
