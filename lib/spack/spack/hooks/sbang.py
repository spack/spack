# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import filecmp
import os
import re
import stat
import sys

import llnl.util.filesystem as fs
import llnl.util.tty as tty
from llnl.util.lang import elide_list

import spack.paths
import spack.store

#: OS-imposed character limit for shebang line: 127 for Linux; 511 for Mac.
#: Different Linux distributions have different limits, but 127 is the
#: smallest among all modern versions.
if sys.platform == 'darwin':
    shebang_limit = 511
else:
    shebang_limit = 127


def sbang_install_path():
    """Location sbang should be installed within Spack's ``install_tree``."""
    sbang_root = str(spack.store.unpadded_root)
    return os.path.join(sbang_root, "bin", "sbang")


def sbang_shebang_line(use_sbang_in_PATH=False):
    """Full shebang line that should be prepended to files to use sbang.

    The line returned does not have a final newline (caller should add it
    if needed).

    This should be the only place in Spack that knows about what
    interpreter we use for ``sbang``.
    """
    if use_sbang_in_PATH:
        return '#!/usr/bin/env sbang'
    else:
        return '#!/bin/sh %s' % sbang_install_path()


def sbang_shebang_itself_too_long():
    """When sbang itself is installed in a very long path, we can't use its absolute
    path to shorten shebang lines. This function tests if that is the case."""
    return len(sbang_shebang_line()) > shebang_limit


def shebang_too_long(path):
    """Detects whether a file has a shebang line that is too long."""
    try:
        with open(path, 'rb') as script:
            bytes = script.read(2)
            if bytes != b'#!':
                return False

            return len(bytes) + len(script.readline()) > shebang_limit
    except (OSError, IOError):
        return False


def filter_shebang(path, use_sbang_in_PATH):
    """Adds a second shebang line, using sbang, at the beginning of a file."""
    with open(path, 'rb') as original_file:
        original = original_file.read()
        if sys.version_info >= (2, 7):
            original = original.decode(encoding='UTF-8')
        else:
            original = original.decode('UTF-8')

    # This line will be prepended to file
    new_sbang_line = '%s\n' % sbang_shebang_line(use_sbang_in_PATH)

    # Skip files that are already using sbang.
    if original.startswith(new_sbang_line):
        return

    # In the following, newlines have to be excluded in the regular expression
    # else any mention of "lua" in the document will lead to spurious matches.

    # Use --! instead of #! on second line for lua.
    if re.search(r'^#!(/[^/\n]*)*lua\b', original):
        original = re.sub(r'^#', '--', original)

    # Use <?php #! instead of #! on second line for php.
    if re.search(r'^#!(/[^/\n]*)*php\b', original):
        original = re.sub(r'^#', '<?php #', original) + ' ?>'

    # Use //! instead of #! on second line for node.js.
    if re.search(r'^#!(/[^/\n]*)*node\b', original):
        original = re.sub(r'^#', '//', original)

    # Change non-writable files to be writable if needed.
    saved_mode = None
    if not os.access(path, os.W_OK):
        st = os.stat(path)
        saved_mode = st.st_mode
        os.chmod(path, saved_mode | stat.S_IWRITE)

    with open(path, 'wb') as new_file:
        if sys.version_info >= (2, 7):
            new_file.write(new_sbang_line.encode(encoding='UTF-8'))
            new_file.write(original.encode(encoding='UTF-8'))
        else:
            new_file.write(new_sbang_line.encode('UTF-8'))
            new_file.write(original.encode('UTF-8'))

    # Restore original permissions.
    if saved_mode is not None:
        os.chmod(path, saved_mode)

    tty.debug("Patched overlong shebang in %s" % path)


def filter_shebangs_in_directory(directory):
    patched_files = []

    # Switch to /usr/bin/env sbang when sbang is installed in a long path itself.
    use_sbang_in_PATH = sbang_shebang_itself_too_long()

    for (root, _, filenames) in os.walk(directory):
        for file in filenames:
            path = os.path.join(root, file)

            # skip over files that don't need to be patched.
            if os.path.islink(path) or not shebang_too_long(path):
                continue

            filter_shebang(path, use_sbang_in_PATH)
            patched_files.append(file)

    return patched_files


def install_sbang():
    """Ensure that ``sbang`` is installed in the root of Spack's install_tree.

    This is the shortest known publicly accessible path, and installing
    ``sbang`` here ensures that users can access the script and that
    ``sbang`` itself is in a short path.
    """
    # copy in a new version of sbang if it differs from what's in spack
    sbang_path = sbang_install_path()
    if os.path.exists(sbang_path) and filecmp.cmp(
            spack.paths.sbang_script, sbang_path):
        return

    # make $install_tree/bin and copy in a new version of sbang if needed
    sbang_bin_dir = os.path.dirname(sbang_path)
    fs.mkdirp(sbang_bin_dir)
    fs.install(spack.paths.sbang_script, sbang_path)
    fs.set_install_permissions(sbang_bin_dir)


def filter_shebangs_in_directory_and_warn(directory):
    paths = filter_shebangs_in_directory(directory)

    if not (paths and sbang_shebang_itself_too_long()):
        return

    short_list = elide_list(paths, 4)
    sbang_bin = os.path.dirname(sbang_install_path())
    tty.warn("Failed to shorten shebang lines of {0} files {1}, because sbang's "
             "install path ({2}) is too long. For the installation to work, it is "
             "required to have sbang in your PATH. Alternatively, you can shorten the "
             "install root (config:install_tree:root).".format(
                 len(paths), short_list, sbang_bin))


def post_install(spec):
    """This hook edits scripts so that they call /bin/bash
    $spack_prefix/bin/sbang instead of something longer than the
    shebang limit.
    """
    if spec.external:
        tty.debug('SKIP: shebang filtering [external package]')
        return

    install_sbang()
    filter_shebangs_in_directory_and_warn(spec.prefix)
