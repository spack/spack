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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-ont-fast5-api
#
# You can edit this file again by typing:
#
#     spack edit py-ont-fast5-api
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class PyOntFast5Api(PythonPackage):
    """
This project provides classes and utility functions for working with read fast5
files. It provides an abstraction layer between the underlying h5py library and
the various concepts central to read fast5 files, such as "reads", "analyses",
"analysis summaries", and "analysis datasets". Ideally all interaction with a
read fast5 file should be possible via this API, without having to directly
invoke the h5py library.."""

    homepage = "https://github.com/nanoporetech/ont_fast5_api"
    url      = "https://pypi.python.org/packages/fb/eb/97b3e279270f59c0f0bcca328a6c036d8f29910821925588a5e0c2dbca57/ont-fast5-api-0.3.2.tar.gz"

    version('0.3.2', '2ccfdbcd55239ffae712bb6e70ebfe8c')
    
    extends('python')

    depends_on('py-setuptools', type='build')

