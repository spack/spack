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
from llnl.util.filesystem import mkdirp


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
        self._root = source_root


    def traverse(self, dest_root, **kwargs):
        """Traverse LinkTree root and dest simultaneously.

        Walks the LinkTree directory in pre or post order.  Yields
        each file in the source directory with a matching path from
        the dest directory.  e.g., for this tree::

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
                              src that do not exit in dest.

        """
        # Yield directories before or after their contents.
        order  = kwargs.get('order', 'pre')
        if order not in ('pre', 'post'):
            raise ValueError("Order must be 'pre' or 'post'.")

        # List of relative paths to ignore under the src root.
        ignore = kwargs.get('ignore', lambda filename: False)

        # Whether to descend when dirs dont' exist in dest.
        follow_nonexisting = kwargs.get('follow_nonexisting', True)

        for dirpath, dirnames, filenames in os.walk(self._root):
            rel_path  = dirpath[len(self._root):]
            rel_path = rel_path.lstrip(os.path.sep)
            dest_dirpath = os.path.join(dest_root, rel_path)

            # Don't descend into ignored directories
            if ignore(dest_dirpath):
                return

            # Don't descend into dirs in dest that do not exist in src.
            if not follow_nonexisting:
                dirnames[:] = [
                    d for d in dirnames
                    if os.path.exists(os.path.join(dest_dirpath, d))]

            # preorder yields directories before children
            if order == 'pre':
                yield (dirpath, dest_dirpath)

            for name in filenames:
                src_file  = os.path.join(dirpath, name)
                dest_file = os.path.join(dest_dirpath, name)

                # Ignore particular paths inside the install root.
                src_relpath = src_file[len(self._root):]
                src_relpath = src_relpath.lstrip(os.path.sep)
                if ignore(src_relpath):
                    continue

                yield (src_file, dest_file)

            # postorder yields directories after children
            if order == 'post':
                yield (dirpath, dest_dirpath)



    def find_conflict(self, dest_root, **kwargs):
        """Returns the first file in dest that also exists in src."""
        kwargs['follow_nonexisting'] = False
        for src, dest in self.traverse(dest_root, **kwargs):
            if os.path.exists(dest) and not os.path.isdir(dest):
                return dest
        return None


    def merge(self, dest_root, **kwargs):
        """Link all files in src into dest, creating directories if necessary."""
        kwargs['order'] = 'pre'
        for src, dest in self.traverse(dest_root, **kwargs):
            if os.path.isdir(src):
                mkdirp(dest)
            else:
                assert(not os.path.exists(dest))
                os.symlink(src, dest)


    def unmerge(self, dest_root, **kwargs):
        """Unlink all files in dest that exist in src.

        Unlinks directories in dest if they are empty.

        """
        kwargs['order'] = 'post'
        for src, dest in self.traverse(dest_root, **kwargs):
            if os.path.isdir(dest):
                if not os.listdir(dest):
                    # TODO: what if empty directories were present pre-merge?
                    shutil.rmtree(dest, ignore_errors=True)

            elif os.path.exists(dest):
                if not os.path.islink(dest):
                    raise ValueError("%s is not a link tree!" % dest)
                os.remove(dest)
