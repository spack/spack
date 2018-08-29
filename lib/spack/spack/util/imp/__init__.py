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
"""Consolidated module for all imports done by Spack.

Many parts of Spack have to import Python code. This utility package
wraps Spack's interface with Python's import system.

We do this because Python's import system is confusing and changes from
Python version to Python version, and we should be able to adapt our
approach to the underlying implementation.

Currently, this uses ``importlib.machinery`` where available and ``imp``
when ``importlib`` is not completely usable.
"""

try:
    from .importlib_importer import load_source  # noqa
except ImportError:
    from .imp_importer import load_source        # noqa
