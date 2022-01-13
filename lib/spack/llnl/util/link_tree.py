# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""LinkTree class for setting up trees of symbolic links."""

from __future__ import print_function

import filecmp
import os
import shutil

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp, touch, traverse_tree

__all__ = ['LinkTree']

empty_file_name = '.spack-empty'


def remove_link(src, dest):
    if not os.path.islink(dest):
        raise ValueError("%s is not a link tree!" % dest)
    # remove if dest is a hardlink/symlink to src; this will only
    # be false if two packages are merged into a prefix and have a
    # conflicting file
    if filecmp.cmp(src, dest, shallow=True):
        os.remove(dest)


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

    def find_conflict(self, dest_root, ignore=None,
                      ignore_file_conflicts=False):
        """Returns the first file in dest that conflicts with src"""
        ignore = ignore or (lambda x: False)
        conflicts = self.find_dir_conflicts(dest_root, ignore)

        if not ignore_file_conflicts:
            conflicts.extend(
                dst for src, dst
                in self.get_file_map(dest_root, ignore).items()
                if os.path.exists(dst))

        if conflicts:
            return conflicts[0]

    def find_dir_conflicts(self, dest_root, ignore):
        conflicts = []
        kwargs = {'follow_nonexisting': False, 'ignore': ignore}
        for src, dest in traverse_tree(self._root, dest_root, **kwargs):
            if os.path.isdir(src):
                if os.path.exists(dest) and not os.path.isdir(dest):
                    conflicts.append("File blocks directory: %s" % dest)
            elif os.path.exists(dest) and os.path.isdir(dest):
                conflicts.append("Directory blocks directory: %s" % dest)
        return conflicts

    def get_file_map(self, dest_root, ignore):
        merge_map = {}
        kwargs = {'follow_nonexisting': True, 'ignore': ignore}
        for src, dest in traverse_tree(self._root, dest_root, **kwargs):
            if not os.path.isdir(src):
                merge_map[src] = dest
        return merge_map

    def merge_directories(self, dest_root, ignore):
        for src, dest in traverse_tree(self._root, dest_root, ignore=ignore):
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

    def unmerge_directories(self, dest_root, ignore):
        for src, dest in traverse_tree(
                self._root, dest_root, ignore=ignore, order='post'):
            if os.path.isdir(src):
                if not os.path.exists(dest):
                    continue
                elif not os.path.isdir(dest):
                    raise ValueError("File blocks directory: %s" % dest)

                # remove directory if it is empty.
                if not os.listdir(dest):
                    shutil.rmtree(dest, ignore_errors=True)

                # remove empty dir marker if present.
                marker = os.path.join(dest, empty_file_name)
                if os.path.exists(marker):
                    os.remove(marker)

    def merge(self, dest_root, ignore_conflicts=False, ignore=None,
              link=os.symlink, relative=False):
        """Link all files in src into dest, creating directories
           if necessary.

        Keyword Args:

        ignore_conflicts (bool): if True, do not break when the target exists;
            return a list of files that could not be linked

        ignore (callable): callable that returns True if a file is to be
            ignored in the merge (by default ignore nothing)

        link (callable): function to create links with (defaults to os.symlink)

        relative (bool): create all symlinks relative to the target
            (default False)

        """
        if ignore is None:
            ignore = lambda x: False

        conflict = self.find_conflict(
            dest_root, ignore=ignore, ignore_file_conflicts=ignore_conflicts)
        if conflict:
            raise MergeConflictError(conflict)

        self.merge_directories(dest_root, ignore)
        existing = []
        for src, dst in self.get_file_map(dest_root, ignore).items():
            if os.path.exists(dst):
                existing.append(dst)
            elif relative:
                abs_src = os.path.abspath(src)
                dst_dir = os.path.dirname(os.path.abspath(dst))
                rel = os.path.relpath(abs_src, dst_dir)
                link(rel, dst)
            else:
                link(src, dst)

        for c in existing:
            tty.warn("Could not merge: %s" % c)

    def unmerge(self, dest_root, ignore=None, remove_file=remove_link):
        """Unlink all files in dest that exist in src.

        Unlinks directories in dest if they are empty.
        """
        if ignore is None:
            ignore = lambda x: False

        for src, dst in self.get_file_map(dest_root, ignore).items():
            remove_file(src, dst)
        self.unmerge_directories(dest_root, ignore)


class MergeConflictError(Exception):

    def __init__(self, path):
        super(MergeConflictError, self).__init__(
            "Package merge blocked by file: %s" % path)
