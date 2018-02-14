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

    def merge(self, dest_root, link=os.symlink, **kwargs):
        """Link all files in src into dest, creating directories
           if necessary.
           If ignore_conflicts is True, do not break when the target exists but
           rather return a list of files that could not be linked.
           Note that files blocking directories will still cause an error.
        """
        kwargs['order'] = 'pre'
        ignore_conflicts = kwargs.get("ignore_conflicts", False)
        existing = []
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
                if os.path.exists(dest):
                    if ignore_conflicts:
                        existing.append(src)
                    else:
                        raise AssertionError("File already exists: %s" % dest)
                else:
                    link(src, dest)
        if ignore_conflicts:
            return existing

    def unmerge(self, dest_root, **kwargs):
        """Unlink all files in dest that exist in src.

        Unlinks directories in dest if they are empty.

        """
        kwargs['order'] = 'post'
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
                if not os.path.islink(dest):
                    raise ValueError("%s is not a link tree!" % dest)
                # remove if dest is a hardlink/symlink to src; this will only
                # be false if two packages are merged into a prefix and have a
                # conflicting file
                if filecmp.cmp(src, dest, shallow=True):
                    os.remove(dest)
