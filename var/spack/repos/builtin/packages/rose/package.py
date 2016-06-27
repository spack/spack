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
#------------------------------------------------------------------------------
# Author: Justin Too <too1@llnl.gov>
#------------------------------------------------------------------------------

from spack import *

class Rose(Package):
    """A compiler infrastructure to build source-to-source program
       transformation and analysis tools.
       (Developed at Lawrence Livermore National Lab)"""

    homepage = "http://rosecompiler.org/"
    url      = "https://github.com/rose-compiler/edg4x-rose"

    version('master', branch='master', git='https://github.com/rose-compiler/edg4x-rose.git')

    patch('add_spack_compiler_recognition.patch')

    depends_on("autoconf@2.69")
    depends_on("automake@1.14")
    depends_on("libtool@2.4")
    depends_on("boost@1.54.0")
    depends_on("jdk@8u25-linux-x64")

    def install(self, spec, prefix):
        # Bootstrap with autotools
        bash = which('bash')
        bash('build')

        # Configure, compile & install
        with working_dir('rose-build', create=True):
            boost = spec['boost']

            configure = Executable('../configure')
            configure("--prefix=" + prefix,
                      "--with-boost=" + boost.prefix,
                      "--disable-boost-version-check")
            make("install-core")

