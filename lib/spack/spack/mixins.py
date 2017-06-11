##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import os

import llnl.util.filesystem


class FilterCompilerWrappers(object):
    """This mixin class registers a callback that filters a list of files
    after installation and substitutes hardcoded paths pointing to the Spack
    compiler wrappers with the corresponding 'real' compilers.
    """

    #: compiler wrappers to be filtered (needs to be overridden)
    to_be_filtered_for_wrappers = []

    #: phase after which the callback is invoked (default 'install')
    filter_phase = 'install'

    def __init__(self):

        attr_name = '_InstallPhase_{0}'.format(self.filter_phase)

        # Here we want to get the attribute directly from the class (not from
        # the instance), so that we can modify it and add the mixin method
        phase = getattr(type(self), attr_name)

        # Due to MRO, we may have taken a method from a parent class
        # and modifying it may influence other packages in unwanted manners.
        # Solve the problem by copying the phase into the most derived class.
        setattr(type(self), attr_name, phase.copy())
        phase = getattr(type(self), attr_name)

        phase.run_after.append(
            FilterCompilerWrappers.filter_compilers
        )

        super(FilterCompilerWrappers, self).__init__()

    def filter_compilers(self):
        """Substitutes any path referring to a Spack compiler wrapper
        with the path of the underlying compiler that has been used.

        If this isn't done, the files will have CC, CXX, F77, and FC set
        to Spack's generic cc, c++, f77, and f90.  We want them to
        be bound to whatever compiler they were built with.
        """

        kwargs = {'ignore_absent': True, 'backup': False, 'string': True}

        if self.to_be_filtered_for_wrappers:
            x = llnl.util.filesystem.FileFilter(
                *self.to_be_filtered_for_wrappers
            )

            x.filter(os.environ['CC'], self.compiler.cc, **kwargs)
            x.filter(os.environ['CXX'], self.compiler.cxx, **kwargs)
            x.filter(os.environ['F77'], self.compiler.f77, **kwargs)
            x.filter(os.environ['FC'], self.compiler.fc, **kwargs)

            # Remove this linking flag if present (it turns RPATH into RUNPATH)
            x.filter('-Wl,--enable-new-dtags', '', **kwargs)
