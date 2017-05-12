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
#     spack install ont-albacore
#
# You can edit this file again by typing:
#
#     spack edit ont-albacore
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
import glob
from spack import *


class OntAlbacore(Package):
    """FIXME: The Albacore Basecaller."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://nanoporetech.com"
    url      = "https://mirror.oxfordnanoportal.com/software/analysis/ont_albacore-1.1.0-cp35-cp35m-manylinux1_x86_64.whl"

    version('1.1.0', 'fab4502ea1bad99d813aa2629e03e83d', expand=False)

    extends('python')

    depends_on('python@3.5.2',        type=('build', 'run'))
    depends_on('py-setuptools',        type=('build', 'run'))
    depends_on('py-six',        type=('build', 'run'))
    depends_on('py-numpy',        type=('build', 'run'))
    depends_on('py-dateutil',        type=('build', 'run'))
    depends_on('py-h5py',        type=('build', 'run'))
    depends_on('py-ont-fast5-api',        type=('build', 'run'))
    depends_on('py-pip',        type=('build', 'run'))
    depends_on('py-packaging',        type=('build', 'run'))
    depends_on('py-pyparsing',        type=('build', 'run'))
    depends_on('py-appdirs',        type=('build', 'run'))

    def install(self, spec, prefix):
        wheel = glob.glob('*.whl')[0]
        pip = which('pip')
        pip('install', '--prefix={0}'.format(prefix), wheel)
