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
from spack import *


class Masa(AutotoolsPackage):
    """MASA (Manufactured Analytical Solution Abstraction) is a library
       written in C++ (with C, python and Fortran90 interfaces) which
       provides a suite of manufactured solutions for the software
       verification of partial differential equation solvers in multiple
       dimensions."""

    homepage = "https://github.com/manufactured-solutions/MASA"
    git      = "https://github.com/manufactured-solutions/MASA.git"

    version('master', tag='master')

    variant('fortran', default=True,
            description='Compile with Fortran interfaces')
    variant('python',  default=True,
            description='Compile with Python interfaces')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('swig',     type='build')
    depends_on('python', when='+python')
    depends_on('metaphysicl')

    def configure_args(self):
        options = []

        options.extend([
            '--with-metaphysicl=%s' % self.spec['metaphysicl'].prefix
        ])

        if '+fortran' in self.spec:
            options.extend(['--enable-fortran-interfaces'])

        if '+python' in self.spec:
            options.extend(['--enable-python-interfaces'])

        return options
