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
"""Implementation of Spack imports that uses importlib underneath.

``importlib`` is only fully implemented in Python 3.
"""
from importlib.machinery import SourceFileLoader


class PrependFileLoader(SourceFileLoader):
    def __init__(self, full_name, path, prepend=None):
        super(PrependFileLoader, self).__init__(full_name, path)
        self.prepend = prepend

    def get_data(self, path):
        data = super(PrependFileLoader, self).get_data(path)
        if path != self.path or self.prepend is None:
            return data
        else:
            return self.prepend.encode() + b"\n" + data


def load_source(full_name, path, prepend=None):
    """Import a Python module from source.

    Load the source file and add it to ``sys.modules``.

    Args:
        full_name (str): full name of the module to be loaded
        path (str): path to the file that should be loaded
        prepend (str, optional): some optional code to prepend to the
            loaded module; e.g., can be used to inject import statements

    Returns:
        (ModuleType): the loaded module
    """
    # use our custom loader
    loader = PrependFileLoader(full_name, path, prepend)
    return loader.load_module()
