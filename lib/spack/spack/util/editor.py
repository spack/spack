# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Module for finding the user's preferred text editor.

Defines one function, editor(), which invokes the editor defined by the
user's VISUAL environment variable if set. We fall back to the editor
defined by the EDITOR environment variable if VISUAL is not set or the
specified editor fails (e.g. no DISPLAY for a graphical editor). If
neither variable is set, we fall back to one of several common editors,
raising an EnvironmentError if we are unable to find one.
"""
import copy
import os

from spack.util.executable import Executable, which

_visual_exe\
    = Executable(os.environ['VISUAL']) if 'VISUAL' in os.environ else None
_editor_exe\
    = Executable(os.environ['EDITOR']) \
    if 'EDITOR' in os.environ else which('vim', 'vi', 'emacs', 'nano')


# Invoke the user's editor.
def editor(*args, **kwargs):
    if _visual_exe:
        visual_kwargs = copy.copy(kwargs)
        visual_kwargs['fail_on_error'] = False
        _visual_exe(*args, **visual_kwargs)
        if _visual_exe.returncode == 0:
            return  # Otherwise, fall back to EDITOR.

    if _editor_exe:
        _editor_exe(*args, **kwargs)
    else:
        raise EnvironmentError(
            'No text editor found! Please set the VISUAL and/or EDITOR '
            'environment variable(s) to your preferred text editor.')
