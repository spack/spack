# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Module for finding the user's preferred text editor.

Defines one variable: ``editor``, which is a
``spack.util.executable.Executable`` object that can be called to invoke
the editor.

If no ``editor`` is found, an ``EnvironmentError`` is raised when
``editor`` is invoked.
"""
import os

from spack.util.executable import Executable, which

# Set up the user's editor
# $EDITOR environment variable has the highest precedence
editor = os.environ.get('EDITOR')

# if editor is not set, use some sensible defaults
if editor is not None:
    editor = Executable(editor)
else:
    editor = which('vim', 'vi', 'emacs', 'nano')

# If there is no editor, only raise an error if we actually try to use it.
if not editor:
    def editor_not_found(*args, **kwargs):
        raise EnvironmentError(
            'No text editor found! Please set the EDITOR environment variable '
            'to your preferred text editor.')
    editor = editor_not_found
