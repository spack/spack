##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""LinkTree class for setting up trees of symbolic links."""
__all__ = ['LinkTree']

import os
import shutil
from llnl.util.filesystem import *

empty_file_name = '.spack-empty'


def traverse_tree(source_root, dest_root, rel_path='', **kwargs):
    """Traverse two filesystem trees simultaneously.

    Walks the LinkTree directory in pre or post order.  Yields each
    file in the source directory with a matching path from the dest
    directory, along with whether the file is a directory.
    e.g., for this tree::

        root/
          a/
            file1
            file2
          b/
            file3

    When called on dest, this yields::

        ('root',         'dest')
        ('root/a',       'dest/a')
        ('root/a/file1', 'dest/a/file1')
        ('root/a/file2', 'dest/a/file2')
        ('root/b',       'dest/b')
        ('root/b/file3', 'dest/b/file3')

    Optional args:

    order=[pre|post] -- Whether to do pre- or post-order traveral.

    ignore=<predicate> -- Predicate indicating which files to ignore.

    follow_nonexisting -- Whether to descend into directories in
                          src that do not exit in dest. Default True.

    follow_links -- Whether to descend into symlinks in src.

    """
    follow_nonexisting = kwargs.get('follow_nonexisting', True)
    follow_links = kwargs.get('follow_link', False)

    # Yield in pre or post order?
    order  = kwargs.get('order', 'pre')
    if order not in ('pre', 'post'):
        raise ValueError("Order must be 'pre' or 'post'.")

    # List of relative paths to ignore under the src root.
    ignore = kwargs.get('ignore', lambda filename: False)

    # Don't descend into ignored directories
    if ignore(rel_path):
        return

    source_path = os.path.join(source_root, rel_path)
    dest_path   = os.path.join(dest_root, rel_path)

    # preorder yields directories before children
    if order == 'pre':
        yield (source_path, dest_path)

    for f in os.listdir(source_path):
        source_child = os.path.join(source_path, f)
        dest_child   = os.path.join(dest_path, f)
        rel_child    = os.path.join(rel_path, f)

        # Treat as a directory
        if os.path.isdir(source_child) and (
            follow_links or not os.path.islink(source_child)):

            # When follow_nonexisting isn't set, don't descend into dirs
            # in source that do not exist in dest
            if follow_nonexisting or os.path.exists(dest_child):
                tuples = traverse_tree(source_root, dest_root, rel_child, **kwargs)
                for t in tuples: yield t

        # Treat as a file.
        elif not ignore(os.path.join(rel_path, f)):
            yield (source_child, dest_child)

    if order == 'post':
        yield (source_path, dest_path)



class LinkTree(object):
    """Class to create trees of symbolic links from a source directory.

    LinkTree objects are constructed with a source root.  Their
    methods allow you to create and delete trees of symbolic links
    back to the source tree in specific destination directories.
    Trees comprise symlinks only to files; directries are never
    symlinked to, to prevent the source directory from ever being
    modified.

    """
    def __init__(self, source_root):
        if not os.path.exists(source_root):
            raise IOError("No such file or directory: '%s'", source_root)

        self._root = source_root


    def find_conflict(self, dest_root, **kwargs):
        """Returns the first file in dest that conflicts with src"""
        kwargs['follow_nonexisting'] = False
        for src, dest in traverse_tree(self._root, dest_root, **kwargs):
            if os.path.isdir(src):
                if os.path.exists(dest) and not os.path.isdir(dest):
                    return dest
            elif os.path.exists(dest):
                return dest
        return None


    def merge(self, dest_root, **kwargs):
        """Link all files in src into dest, creating directories if necessary."""
        kwargs['order'] = 'pre'
        for src, dest in traverse_tree(self._root, dest_root, **kwargs):
            if os.path.isdir(src):
                if not os.path.exists(dest):
                    mkdirp(dest)
                    continue

                if not os.path.isdir(dest):
                    raise ValueError("File blocks directory: %s" % dest)

                # mark empty directories so they aren't removed on unmerge.
                if not os.listdir(dest):
                    marker = os.path.join(dest, empty_file_name)
                    touch(marker)

            else:
                assert(not os.path.exists(dest))
                os.symlink(src, dest)


    def unmerge(self, dest_root, **kwargs):
        """Unlink all files in dest that exist in src.

        Unlinks directories in dest if they are empty.

        """
        kwargs['order'] = 'post'
        for src, dest in traverse_tree(self._root, dest_root, **kwargs):
            if os.path.isdir(src):
                if not os.path.isdir(dest):
                    raise ValueError("File blocks directory: %s" % dest)

                # remove directory if it is empty.
                if not os.listdir(dest):
                    shutil.rmtree(dest, ignore_errors=True)

                # remove empty dir marker if present.
                marker = os.path.join(dest, empty_file_name)
                if os.path.exists(marker):
                    os.remove(marker)

            elif os.path.exists(dest):
                if not os.path.islink(dest):
                    raise ValueError("%s is not a link tree!" % dest)
                os.remove(dest)
