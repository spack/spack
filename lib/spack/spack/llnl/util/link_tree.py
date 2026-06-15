# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""LinkTree class for setting up trees of symbolic links."""

import filecmp
import os
import shutil
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union

import spack.llnl.util.filesystem as fs
import spack.llnl.util.tty as tty

__all__ = ["LinkTree"]

empty_file_name = ".spack-empty"


def remove_link(src, dest):
    if not fs.islink(dest):
        raise ValueError("%s is not a link tree!" % dest)
    # remove if dest is a hardlink/symlink to src; this will only
    # be false if two packages are merged into a prefix and have a
    # conflicting file
    if filecmp.cmp(src, dest, shallow=True):
        os.remove(dest)


class MergeConflict:
    """
    The invariant here is that src_a and src_b are both mapped
    to dst:

        project(src_a) == project(src_b) == dst
    """

    def __init__(self, dst, src_a=None, src_b=None):
        self.dst = dst
        self.src_a = src_a
        self.src_b = src_b

    def __repr__(self) -> str:
        return f"MergeConflict(dst={self.dst!r}, src_a={self.src_a!r}, src_b={self.src_b!r})"


def _samefile(a: str, b: str):
    try:
        return os.path.samefile(a, b)
    except OSError:
        return False


#: (index, src_root, rel_path, is_symlink)
FileEntry = Tuple[int, str, str, bool]

#: (index, src_root, rel_path)
DirEntry = Tuple[int, str, str]

PrefixAndProjection = Union[Union[str, Path], Tuple[Union[str, Path], Union[str, Path]]]


class MultiPrefixMerger:
    """Class that takes multiple pairs of prefixes and projections, and produces a list of
    directories to create, files to link, and conflicts when merging them together."""

    def __init__(
        self,
        sources: Sequence[PrefixAndProjection],
        ignore: Optional[Callable[[str], bool]] = None,
        normalize_paths: bool = False,
        dir_symlink_optimization: bool = False,
    ):
        """
        Args:
            sources: list of source directories, or tuples of (source directory, projection) pairs
            ignore: optional callable(rel_path) -> bool to skip entries
            normalize_paths: whether to normalize paths for case-insensitive filesystems
            dir_symlink_optimization: whether to enable directory-level symlink optimization
        """
        self.ignore = ignore if ignore is not None else lambda f: False

        # On case-insensitive filesystems, normalize paths to detect duplications
        self.normalize_paths = normalize_paths

        #: Whether to symlink directories unique to one source
        self._dir_symlink_optimization = dir_symlink_optimization

        # When mapping <src root> to <dst root>/<projection>, we need to prepend the <projection>
        # bit to the relative path in the destination dir.
        self.projection: str = ""

        # Two files f and g conflict if they are not os.path.samefile(f, g) and they are both
        # projected to the same destination file. These conflicts are not necessarily fatal, and
        # can be resolved or ignored. For example <prefix>/LICENSE or
        # <site-packages>/<namespace>/__init__.py conflicts can be ignored).
        self.file_conflicts: List[MergeConflict] = []

        # When we have to create a dir where a file is, or a file where a dir is, we have fatal
        # errors, listed here.
        self.fatal_conflicts: List[MergeConflict] = []

        # What directories we have to make; this is an ordered dict, so that we have a fast lookup
        # and can run mkdir in order.
        self.directories: Dict[str, Tuple[str, str]] = {}

        # If the visitor is configured to normalize paths, keep a map of
        # normalized path to: original path, root directory + relative path
        self._directories_normalized: Dict[str, Tuple[str, str, str]] = {}

        # Files to link. Maps dst_rel to (src_root, src_rel). This is an ordered dict, where files
        # are guaranteed to be grouped by src_root in the order they were visited.
        self.files: Dict[str, Tuple[str, str]] = {}

        # If the visitor is configured to normalize paths, keep a map of
        # normalized path to: original path, root directory + relative path
        self._files_normalized: Dict[str, Tuple[str, str, str]] = {}

        # Group sources by projection
        projection_groups: Dict[str, List[str]] = {}
        for src in sources:
            if isinstance(src, tuple):
                src_root, projection = src
            else:
                src_root, projection = src, ""
            projection_groups.setdefault(str(projection), []).append(str(src_root))

        # Process each projection group
        for projection, roots in projection_groups.items():
            self.set_projection(projection)
            active = [(i, root, "") for i, root in enumerate(roots)]
            self._simultaneous_recurse(active, 0)

    def _in_directories(self, proj_rel_path: str) -> bool:
        """
        Check if a path is already in the directory list
        """
        if self.normalize_paths:
            return proj_rel_path.lower() in self._directories_normalized
        else:
            return proj_rel_path in self.directories

    def _directory(self, proj_rel_path: str) -> Tuple[str, str, str]:
        """
        Get the directory that is mapped to a path
        """
        if self.normalize_paths:
            return self._directories_normalized[proj_rel_path.lower()]
        else:
            return (proj_rel_path, *self.directories[proj_rel_path])

    def _del_directory(self, proj_rel_path: str):
        """
        Remove a directory from the list of directories
        """
        del self.directories[proj_rel_path]
        if self.normalize_paths:
            del self._directories_normalized[proj_rel_path.lower()]

    def _add_directory(self, proj_rel_path: str, root: str, rel_path: str):
        """
        Add a directory to the list of directories.
        Also stores the normalized version for later lookups
        """
        self.directories[proj_rel_path] = (root, rel_path)
        if self.normalize_paths:
            self._directories_normalized[proj_rel_path.lower()] = (proj_rel_path, root, rel_path)

    def _in_files(self, proj_rel_path: str) -> bool:
        """
        Check if a path is already in the files list
        """
        if self.normalize_paths:
            return proj_rel_path.lower() in self._files_normalized
        else:
            return proj_rel_path in self.files

    def _file(self, proj_rel_path: str) -> Tuple[str, str, str]:
        """
        Get the file that is mapped to a path
        """
        if self.normalize_paths:
            return self._files_normalized[proj_rel_path.lower()]
        else:
            return (proj_rel_path, *self.files[proj_rel_path])

    def _add_file(self, proj_rel_path: str, root: str, rel_path: str):
        """
        Add a file to the list of files
        Also stores the normalized version for later lookups
        """
        self.files[proj_rel_path] = (root, rel_path)
        if self.normalize_paths:
            self._files_normalized[proj_rel_path.lower()] = (proj_rel_path, root, rel_path)

    def set_projection(self, projection: str) -> None:
        self.projection = os.path.normpath(projection)

        # Todo, is this how to check in general for empty projection?
        if self.projection == ".":
            self.projection = ""
            return

        # If there is a projection, we'll also create the directories
        # it consists of, and check whether that's causing conflicts.
        path = ""
        for part in self.projection.split(os.sep):
            path = os.path.join(path, part)
            if not self._in_files(path):
                self._add_directory(path, "<projection>", path)
            else:
                # Can't create a dir where a file is.
                _, src_a_root, src_a_relpath = self._file(path)
                self.fatal_conflicts.append(
                    MergeConflict(
                        dst=path,
                        src_a=os.path.join(src_a_root, src_a_relpath),
                        src_b=os.path.join("<projection>", path),
                    )
                )

    def _simultaneous_recurse(self, active: List[Tuple[int, str, str]], depth: int) -> None:
        """Recursively scan active sources simultaneously.

        Args:
            depth: current depth from source root (for symlinked dir handling)
            active: list of (index, src_root, rel_path) tuples that have this directory
        """
        # Mapping of normalized entry names to their corresponding directory and file entries
        entry_map: Dict[str, Tuple[List[DirEntry], List[FileEntry]]] = {}

        for idx, src_root, rel_path in active:
            scan_path = os.path.join(src_root, rel_path) if rel_path else src_root
            try:
                scanner = os.scandir(scan_path)
            except OSError:
                continue  # skip if we cannot list directory entries.

            with scanner:
                for dir_entry in scanner:
                    name = dir_entry.name
                    child_rel = os.path.join(rel_path, name) if rel_path else name

                    if self.ignore(child_rel):
                        continue

                    is_link = dir_entry.is_symlink()
                    try:
                        is_dir = dir_entry.is_dir(follow_symlinks=True)
                    except OSError:
                        is_dir = False  # broken symlink is not a dir.

                    norm_name = name.lower() if self.normalize_paths else name
                    dirs, files = entry_map.setdefault(norm_name, ([], []))

                    if is_dir and not is_link:
                        dirs.append((idx, src_root, child_rel))
                    elif is_dir and is_link:
                        if self._should_follow_symlinked_dir(src_root, child_rel, depth):
                            dirs.append((idx, src_root, child_rel))
                        else:
                            files.append((idx, src_root, child_rel, True))
                    else:
                        files.append((idx, src_root, child_rel, is_link))

        # Process collected entries in sorted order
        for norm_name in sorted(entry_map):
            dirs, files = entry_map[norm_name]

            # When dirs and files project to the same path, we have a potential fatal conflict.
            if dirs and files:
                rel_path = dirs[0][2]
                dir_proj = os.path.join(self.projection, rel_path) if self.projection else rel_path
                conflicts = self._dir_file_conflicts(dir_proj, dirs, files)

                if not conflicts:
                    # all files were symlinks to a dir at the same projected location, ignore them.
                    files.clear()
                else:
                    # actual dir-file conflicts we cannot resolve.
                    self.fatal_conflicts.extend(conflicts)
                    continue

            # Note: no elif. We now have either files or dirs.
            if files:
                self._handle_files(files)
            elif dirs and self._handle_dirs(dirs, depth):
                self._simultaneous_recurse(dirs, depth + 1)

    def _should_follow_symlinked_dir(self, src_root: str, rel_path: str, depth: int) -> bool:
        """Determine if a symlinked directory should be followed (treated as real dir)
        or treated as a file."""
        if depth > 1:
            return False
        src = os.path.join(src_root, rel_path)
        real_parent = os.path.realpath(os.path.dirname(src))
        real_child = os.path.realpath(src)
        return real_child.startswith(real_parent)

    def _handle_files(self, files: List[FileEntry]) -> None:
        """Handle file entries that all map to the same projected path."""
        # In case of resolvable conflicts (conflicting files are links to the same file)
        # the best candidate for the source is the non-symlink file.

        _, root, rel_path, is_symlink = files[0]
        dst = os.path.join(self.projection, rel_path) if self.projection else rel_path
        for _, other_root, other_rel_path, other_is_symlink in files[1:]:
            first_path = os.path.join(root, rel_path)
            other_path = os.path.join(other_root, other_rel_path)
            if not _samefile(first_path, other_path):
                # two distinct files project to the same path; this is a conflict.
                self.file_conflicts.append(
                    MergeConflict(dst=dst, src_a=first_path, src_b=other_path)
                )
            elif not other_is_symlink and is_symlink:
                # if they are the same, prefer the non-symlink as the source.
                root, rel_path, is_symlink = other_root, other_rel_path, other_is_symlink
                dst = os.path.join(self.projection, rel_path) if self.projection else rel_path

        self._add_file(dst, root, rel_path)

    def _handle_dirs(self, dirs: List[DirEntry], depth: int) -> bool:
        """Handle directory entries that all map to the same projected path.

        Returns True if the caller should recurse deeper into this directory.
        """
        _, src_root, rel_path = dirs[0]
        proj_child = os.path.join(self.projection, rel_path) if self.projection else rel_path
        if self._dir_symlink_optimization and depth > 0 and len(dirs) == 1:
            # Unique subtree optimization: if this directory is unique to one source, and we're
            # using symlinks, and we're not at the root level, we simply symlink the directory
            # rather than creating it in the view and recursing into it.
            self._add_file(proj_child, src_root, rel_path)
            return False
        else:
            # Subtree optimization not possible, register make dirs operations and recurse.
            self._add_directory(proj_child, src_root, rel_path)
            return True

    def _dir_file_conflicts(
        self, proj_child_rel: str, dirs: List[DirEntry], files: List[FileEntry]
    ) -> Optional[List[MergeConflict]]:
        """Handle dir-file conflicts at the same projected path."""
        # We drop all symlinks that resolve to any of the directories that project to the same path
        # For example the symlink `<prefix a>/include -> <prefix b>/include` is a resolvable
        # conflict as we just keep `<view>/include` in the view. Notice that this is a very rare
        # occurrence.
        remaining_files = [
            os.path.join(file_root, file_rel_path)
            for _, file_root, file_rel_path, is_sym in files
            if not is_sym
            or not any(
                _samefile(
                    os.path.join(file_root, file_rel_path), os.path.join(dir_root, dir_rel_path)
                )
                for _, dir_root, dir_rel_path in dirs
            )
        ]
        if not remaining_files:
            return None
        # Use the first dir is the representative dir to register conflicts.
        _, src_root, rel_path = dirs[0]
        dir_src = os.path.join(src_root, rel_path)
        return [
            MergeConflict(dst=proj_child_rel, src_a=dir_src, src_b=file_path)
            for file_path in remaining_files
        ]


class DestinationMergeVisitor(fs.BaseDirectoryVisitor):
    """DestinationMergeVisitor takes a MultiPrefixMerger and:

    a. registers additional conflicts when merging to the destination prefix
    b. removes redundant mkdir operations when directories already exist in the destination prefix.

    This also makes sure that symlinked directories in the target prefix will never be merged with
    directories in the sources directories.
    """

    def __init__(self, source_merge_visitor: MultiPrefixMerger):
        self.src = source_merge_visitor

    def before_visit_dir(self, root: str, rel_path: str, depth: int) -> bool:
        # If destination dir is a file in a src dir, add a conflict,
        # and don't traverse deeper
        if self.src._in_files(rel_path):
            _, src_a_root, src_a_relpath = self.src._file(rel_path)
            self.src.fatal_conflicts.append(
                MergeConflict(
                    rel_path, os.path.join(src_a_root, src_a_relpath), os.path.join(root, rel_path)
                )
            )
            return False

        # If destination dir was also a src dir, remove the mkdir
        # action, and traverse deeper.
        if self.src._in_directories(rel_path):
            existing_proj_rel_path, _, _ = self.src._directory(rel_path)
            self.src._del_directory(existing_proj_rel_path)
            return True

        # If the destination dir does not appear in the src dir,
        # don't descend into it.
        return False

    def before_visit_symlinked_dir(self, root: str, rel_path: str, depth: int) -> bool:
        """
        Symlinked directories in the destination prefix should
        be seen as files; we should not accidentally merge
        source dir with a symlinked dest dir.
        """

        self.visit_file(root, rel_path, depth)

        # Never descend into symlinked target dirs.
        return False

    def visit_file(self, root: str, rel_path: str, depth: int) -> None:
        # Can't merge a file if target already exists
        if self.src._in_directories(rel_path):
            _, src_a_root, src_a_relpath = self.src._directory(rel_path)
            self.src.fatal_conflicts.append(
                MergeConflict(
                    rel_path, os.path.join(src_a_root, src_a_relpath), os.path.join(root, rel_path)
                )
            )

        elif self.src._in_files(rel_path):
            _, src_a_root, src_a_relpath = self.src._file(rel_path)
            self.src.fatal_conflicts.append(
                MergeConflict(
                    rel_path, os.path.join(src_a_root, src_a_relpath), os.path.join(root, rel_path)
                )
            )

    def visit_symlinked_file(self, root: str, rel_path: str, depth: int) -> None:
        # Treat symlinked files as ordinary files (without "dereferencing")
        self.visit_file(root, rel_path, depth)


class LinkTree:
    """Class to create trees of symbolic links from a source directory.

    LinkTree objects are constructed with a source root.  Their
    methods allow you to create and delete trees of symbolic links
    back to the source tree in specific destination directories.
    Trees comprise symlinks only to files; directories are never
    symlinked to, to prevent the source directory from ever being
    modified.
    """

    def __init__(self, source_root):
        if not os.path.exists(source_root):
            raise OSError("No such file or directory: '%s'", source_root)

        self._root = source_root

    def find_conflict(self, dest_root, ignore=None, ignore_file_conflicts=False):
        """Returns the first file in dest that conflicts with src"""
        ignore = ignore or (lambda x: False)
        conflicts = self.find_dir_conflicts(dest_root, ignore)

        if not ignore_file_conflicts:
            conflicts.extend(
                dst
                for src, dst in self.get_file_map(dest_root, ignore).items()
                if os.path.exists(dst)
            )

        if conflicts:
            return conflicts[0]

    def find_dir_conflicts(self, dest_root, ignore):
        conflicts = []
        kwargs = {"follow_nonexisting": False, "ignore": ignore}
        for src, dest in fs.traverse_tree(self._root, dest_root, **kwargs):
            if os.path.isdir(src):
                if os.path.exists(dest) and not os.path.isdir(dest):
                    conflicts.append("File blocks directory: %s" % dest)
            elif os.path.exists(dest) and os.path.isdir(dest):
                conflicts.append("Directory blocks directory: %s" % dest)
        return conflicts

    def get_file_map(self, dest_root, ignore):
        merge_map = {}
        kwargs = {"follow_nonexisting": True, "ignore": ignore}
        for src, dest in fs.traverse_tree(self._root, dest_root, **kwargs):
            if not os.path.isdir(src):
                merge_map[src] = dest
        return merge_map

    def merge_directories(self, dest_root, ignore):
        for src, dest in fs.traverse_tree(self._root, dest_root, ignore=ignore):
            if os.path.isdir(src):
                if not os.path.exists(dest):
                    fs.mkdirp(dest)
                    continue

                if not os.path.isdir(dest):
                    raise ValueError("File blocks directory: %s" % dest)

                # mark empty directories so they aren't removed on unmerge.
                if not os.listdir(dest):
                    marker = os.path.join(dest, empty_file_name)
                    fs.touch(marker)

    def unmerge_directories(self, dest_root, ignore):
        for src, dest in fs.traverse_tree(self._root, dest_root, ignore=ignore, order="post"):
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

    def merge(
        self,
        dest_root,
        ignore_conflicts: bool = False,
        ignore: Optional[Callable[[str], bool]] = None,
        link: Callable = fs.symlink,
        relative: bool = False,
    ):
        """Link all files in src into dest, creating directories if necessary.

        Arguments:

            ignore_conflicts: if True, do not break when the target exists; return a list of files
                that could not be linked

            ignore: callable that returns True if a file is to be ignored in the merge (by default
                ignore nothing)

            link: function to create links with (defaults to
                ``spack.llnl.util.filesystem.symlink``)

            relative: create all symlinks relative to the target (default False)
        """
        if ignore is None:
            ignore = lambda x: False

        conflict = self.find_conflict(
            dest_root, ignore=ignore, ignore_file_conflicts=ignore_conflicts
        )
        if conflict:
            raise SingleMergeConflictError(conflict)

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
    pass


class ConflictingSpecsError(MergeConflictError):
    def __init__(self, spec_1, spec_2):
        super().__init__(spec_1, spec_2)


class SingleMergeConflictError(MergeConflictError):
    def __init__(self, path):
        super().__init__("Package merge blocked by file: %s" % path)


class MergeConflictSummary(MergeConflictError):
    def __init__(self, conflicts):
        """
        A human-readable summary of file system view merge conflicts (showing only the
        first 3 issues.)
        """
        msg = "{0} fatal error(s) when merging prefixes:".format(len(conflicts))
        # show the first 3 merge conflicts.
        for conflict in conflicts[:3]:
            msg += "\n    `{0}` and `{1}` both project to `{2}`".format(
                conflict.src_a, conflict.src_b, conflict.dst
            )
        super().__init__(msg)
