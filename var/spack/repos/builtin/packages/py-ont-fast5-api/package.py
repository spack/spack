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


class PyOntFast5Api(PythonPackage):
    """This project provides classes and utility functions for working with
    read fast5 files. It provides an abstraction layer between the underlying
    h5py library and the various concepts central to read fast5 files, such as
    "reads", "analyses", "analysis summaries", and "analysis datasets".
    Ideally all interaction with a read fast5 file should be possible via this
    API, without having to directly invoke the h5py library."""

    homepage = "https://github.com/nanoporetech/ont_fast5_api"
    url      = "https://pypi.io/packages/source/o/ont-fast5-api/ont-fast5-api-0.3.2.tar.gz"

    version('0.3.2', '2ccfdbcd55239ffae712bb6e70ebfe8c')

    depends_on('py-setuptools', type='build')
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-numpy@1.8.1:', type=('build', 'run'))
