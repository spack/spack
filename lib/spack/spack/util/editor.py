##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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
