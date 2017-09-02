##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install slatec
#
# You can edit this file again by typing:
#
#     spack edit slatec
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Slatec(MakefilePackage):
    """A comprehensive software library containing over 1400 general purpose 
       mathematical and statistical routines written in Fortran 77."""

    homepage = "http://www.netlib.org/slatec"
    url      = "http://www.netlib.org/slatec/slatec_src.tgz"

    # FIXME: Add proper versions and checksums here.
    version('4.1', 'f7188cf8c3cc39a65600aabca09490ce')

    def edit(self, spec, prefix):
       # slatec has no makefile, we'll write one:
       mf_text= """
SRC_FILES := $(wildcard *.f)
OBJ_FILES := $(SRC_FILES:.f=.o)
FFLAGS := -g -O3 -fPIC
FC = ftn

all:libslatec.a libslatec.so

libslatec.a: $(OBJ_FILES)
	$(AR) -rv $@ $^

libslatec.so: $(OBJ_FILES)
	$(F77) -shared -o $@ $^

.f.o:
	$(F77) -c $(FFLAGS) $<
"""
       with open('Makefile', 'w') as mf:
         mf.write(mf_text)

    def install(self, spec, prefix):
        make()
        mkdir(prefix.lib)
        install('libslatec.a',  prefix.lib)
        install('libslatec.so', prefix.lib)
