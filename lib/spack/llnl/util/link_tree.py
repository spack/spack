##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
"""LinkTree class for setting up trees of symbolic links."""

import os
import shutil
import filecmp

from llnl.util.filesystem import traverse_tree, mkdirp, touch
import llnl.util.tty as tty
import spack.error

__all__ = ['LinkTree']

empty_file_name = '.spack-empty'


class LinkTree(object):
    """Class to create trees of symbolic links from a source directory.

    LinkTree objects are constructed with a source root.  Their
    methods allow you to create and delete trees of symbolic links
    back to the source tree in specific destination directories.
    Trees comprise symlinks only to files; directries are never
    symlinked to, to prevent the source directory from ever being
    modified.

    """

    def __init__(self, source_root, merge_file=None, check_conflict=None,
                 remove_file=None):
        if not os.path.exists(source_root):
            raise IOError("No such file or directory: '%s'", source_root)

        self._root = source_root
        self.check_conflict = check_conflict or (lambda x: os.path.exists(x))

    def find_conflict(self, dest_root, **kwargs):
        """Returns the first file in dest that conflicts with src"""
        kwargs['follow_nonexisting'] = False
        get_all_conflicts = kwargs.get('all', False)
        conflicts = []
        for src, dest in traverse_tree(self._root, dest_root, **kwargs):
            if os.path.isdir(src):
                if os.path.exists(dest) and not os.path.isdir(dest):
                    conflicts.append(dest)
            elif self.check_conflict(dest):
                conflicts.append(dest)
            if conflicts and not get_all_conflicts:
                return conflicts[0]
        return conflicts

    def merge(self, dest_root, **kwargs):
        """Link all files in src into dest, creating directories
           if necessary.
           If ignore_conflicts is True, do not break when the target exists but
           rather return a list of files that could not be linked.
           Note that files blocking directories will still cause an error.
        """
        kwargs['order'] = 'pre'
        ignore_conflicts = kwargs.get("ignore_conflicts", False)
        existing = []

        if not ignore_conflicts:
            ignore = kwargs.get('ignore', lambda x: False)
            conflict = self.find_conflict(dest_root, ignore=ignore)
            if conflict:
                raise MergeConflictError(conflict)

        merge_file = kwargs.get('merge_file', merge_link)
        merge_map = dict(traverse_tree(self._root, dest_root, **kwargs))
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
                if self.check_conflict(dest):
                    if ignore_conflicts:
                        existing.append(src)
                    else:
                        raise AssertionError("File already exists: %s" % dest)
                else:
                    merge_file(src, dest, merge_map)
        for c in existing:
            tty.warn("Could not merge: %s" % c)

    def unmerge(self, dest_root, **kwargs):
        """Unlink all files in dest that exist in src.

        Unlinks directories in dest if they are empty.

        """
        kwargs['order'] = 'post'
        remove_file = kwargs.get('remove_file', remove_link)
        for src, dest in traverse_tree(self._root, dest_root, **kwargs):
            if os.path.isdir(src):
                # Skip non-existing links.
                if not os.path.exists(dest):
                    continue

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
                remove_file(src, dest)


def merge_link(src, dest, merge_map):
    os.symlink(src, dest)


def remove_link(src, dest):
    if not os.path.islink(dest):
        raise ValueError("%s is not a link tree!" % dest)
    # remove if dest is a hardlink/symlink to src; this will only
    # be false if two packages are merged into a prefix and have a
    # conflicting file
    if filecmp.cmp(src, dest, shallow=True):
        os.remove(dest)


class MergeConflictError(spack.error.SpackError):

    def __init__(self, path):
        super(MergeConflictError, self).__init__(
            "Package merge blocked by file: %s" % path)
