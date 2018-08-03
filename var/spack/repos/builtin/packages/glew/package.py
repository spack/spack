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


class Glew(Package):
    """The OpenGL Extension Wrangler Library."""

    homepage = "http://glew.sourceforge.net/"
    url      = "https://sourceforge.net/projects/glew/files/glew/2.0.0/glew-2.0.0.tgz/download"

    version('2.0.0',  '2a2cd7c98f13854d2fcddae0d2b20411')

    depends_on("cmake", type='build')
    depends_on("gl")

    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)

        with working_dir('build'):
            cmake('./cmake/', *options)

            # https://github.com/Homebrew/legacy-homebrew/issues/22025
            # Note: This file is generated only after cmake is run
            filter_file(r'Requires: glu',
                        (''), '../glew.pc')

            make()
            make("install")
