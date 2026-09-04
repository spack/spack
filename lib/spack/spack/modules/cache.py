# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Keep module caches in sync with the modulepath directories managed by Spack.

Caches are built and cleared by shelling out to the ``module`` command (``module
cachebuild`` and ``module cacheclear``, available in Environment Modules >= 5.3), so
knowledge of the cache file format stays within the module system.
"""

import os
from typing import List, Sequence, Set

import spack.util.module_cmd
from spack.util import tty
from spack.util.string import plural

#: Modulepath directories with pending module file changes, whose cache should be
#: updated by the next call to :py:func:`flush`
_pending_dirs: Set[str] = set()


def register(dirname: str) -> None:
    """Records a modulepath directory whose content changed, so that its module cache
    is updated by the next call to :py:func:`flush`."""
    _pending_dirs.add(dirname)


def flush() -> None:
    """Updates the module cache of every modulepath directory registered since the
    last flush, then clears the pending list.

    Directories that no longer exist are skipped: their cache vanished with them.
    The cache of remaining directories is first cleared, as an obsolete cache file is
    not removed by a cache build, then directories left empty are pruned, and finally
    the cache of those still existing is built with a single ``module cachebuild`` run.
    """
    dirs = sorted(d for d in _pending_dirs if os.path.isdir(d))
    _pending_dirs.clear()
    if not dirs:
        return
    dirs_str = plural(len(dirs), "modulepath directory", "modulepath directories")
    tty.msg(f"Updating module cache in {dirs_str}")
    cacheclear(dirs)
    for dirname in dirs:
        try:
            # Remove modulepath directory if left empty, and its empty parents
            os.removedirs(dirname)
        except OSError:
            pass
    dirs = [d for d in dirs if os.path.isdir(d)]
    if dirs:
        cachebuild(dirs)


def cachebuild(dirs: Sequence[str]) -> None:
    """Builds the module cache of each given modulepath directory, with a single
    ``module cachebuild`` run."""
    _run_module_cmd("cachebuild", *dirs)


def cacheclear(dirs: Sequence[str]) -> None:
    """Clears the module cache of each given modulepath directory, with a single
    ``module cacheclear`` run.

    Since ``module cacheclear`` accepts no directory argument, it is run with a
    ``MODULEPATH`` environment variable set to the given directories only. The
    ``MODULEPATH`` value inherited by the Spack process is ignored, so that only
    caches of Spack-managed directories are cleared.
    """
    environb = dict(os.environb)
    environb[b"MODULEPATH"] = os.fsencode(os.pathsep.join(dirs))
    _run_module_cmd("cacheclear", environb=environb)


def _run_module_cmd(*args: str, environb=None) -> None:
    """Runs a cache-related module sub-command, reporting output and errors."""
    output = spack.util.module_cmd.module(*args, environb=environb)
    error_lines: List[str] = []
    for line in (output or "").splitlines():
        if "ERROR" in line:
            error_lines.append(line)
        elif line:
            tty.debug(line)
    if error_lines:
        tty.warn(
            f"'module {args[0]}' failed (Environment Modules >= 5.3 is required)", *error_lines
        )
