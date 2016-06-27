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

from spack import *
import shutil

class Objconv(Package):
    """Object file converter"""
    homepage = "http://www.agner.org/optimize/"
    url      = "http://www.agner.org/optimize/objconv.zip"

    version('2016-01-16', '03e2e8d5670364a5e6451bc5b43743a8')
    # version('2015-12-09', 'fcf8f01a5683387e17df6d21497d53fa')

    def install(self, spec, prefix):
        # unzip stalls if the unpacked files already exist
        shutil.rmtree('spack-build', ignore_errors=True)
        with working_dir('spack-build', create=True):
            # The downloaded archive contains another archive
            unzip = which('unzip')
            unzip('../source.zip')
            # Create a makefile
            with open('Makefile', 'w') as f:
                f.write("""
CXX = c++ -g -O2
SRCS = $(wildcard *.cpp)
OBJS = $(SRCS:%.cpp=%.o)
objconv: $(OBJS); $(CXX) -o $@ $^
%.o: %.cpp; $(CXX) -c $*.cpp
""")
            make()
            mkdirp(prefix.bin)
            install('objconv', '%s/objconv' % prefix.bin)
