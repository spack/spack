# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import inspect
import os
import pathlib
import warnings

import spack.paths_base as paths_base


def _most_recent_internal_call():
    """If called within an audit for a Python library function, finds
    the most recent spot within Spack's source code that generated
    the call.
    """

    stack = inspect.stack()
    this_file = str(pathlib.Path(__file__).resolve())
    spack_prefix = pathlib.Path(paths_base.prefix).resolve()
    for frame in stack:
        frame_loc = pathlib.Path(frame.filename).resolve()
        if str(frame_loc) != this_file and spack_prefix in frame_loc.parents:
            return frame_loc, frame.lineno

    return None, None


_recorded_accesses = set()


def _attempted_modify_internal(msg):
    loc, line = _most_recent_internal_call()
    if loc:
        if (loc, line) not in _recorded_accesses:
            _recorded_accesses.add((loc, line))
            msg += f" at {loc}:{line}"
            warnings.warn(msg)
    else:
        msg += " (no location)"
        warnings.warn(msg)


def _real(path):
    return pathlib.Path(path).absolute().resolve()


_real_spack_prefix = _real(paths_base.prefix)


def _is_in_spack_prefix(path):
    return _real_spack_prefix in _real(path).parents


def _guard_writes(event, args):
    # Note: this doesn't catch files opened in "r" mode and then
    # later upgraded to "w" mode (e.g. our locks). I think to track
    # that properly we would need to (a) patch builtins.open to
    # map all paths to FDs as they are opened (and delete on close)
    # and (b) audit fcntl.fcntl events, using reverse mapping on
    # FD to check associated path
    if event == "open":
        path, mode = args[:2]
        if not mode:
            # Some internal Python libs can call open(..., mode=None)
            return
        if not isinstance(path, str):
            # Skip instances of open() that function like fdopen
            return
        abs_path = os.path.abspath(path)
        intent_to_modify = bool((set(mode) & set("wax")) or "r+" in mode)
        if _is_in_spack_prefix(path) and intent_to_modify:
            _attempted_modify_internal(f"Open {path} in mode [{mode}]")
    elif event in ["shutil.copyfile", "os.rename", "shutil.move"]:
        _, dst = args[:2]
        if _is_in_spack_prefix(dst):
            _attempted_modify_internal(f"copy dst {str(_real(dst))}")
    elif event == "os.mkdir":
        path = args[0]
        if _is_in_spack_prefix(path):
            _attempted_modify_internal(f"mkdir {str(_real(path))}")


def warn_writes_into_spack():
    import sys

    if sys.version_info[:2] >= (3, 8):
        sys.addaudithook(_guard_writes)  # novermin
    else:
        raise ValueError(
            f"Cannot detect writes for Python {sys.version_info[:2]} (supported in 3.8 and later)"
        )
