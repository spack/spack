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


class PyPynn(PythonPackage):
    """A Python package for simulator-independent specification of neuronal
        network models
    """

    homepage = "http://neuralensemble.org/PyNN/"
    url      = "https://pypi.io/packages/source/P/PyNN/PyNN-0.8.3.tar.gz"
    git      = "https://github.com/NeuralEnsemble/PyNN.git"

    version('0.9.1', '3b8a6c63dc59d7ac751029f84dcaf7e6')
    version('0.8.3', '28c63f898093806a57198e9271ed7b82')
    version('0.8beta', commit='ffb0cb1661f2b0f2778db8f71865978fe7a7a6a4')
    version('0.8.1', '7fb165ed5af35a115cb9c60991645ae6')
    version('0.7.5', 'd8280544e4c9b34b40fd372b16342841')

    depends_on('python@2.6:2.8,3.3:')
    depends_on('py-jinja2@2.7:',        type=('build', 'run'))
    depends_on('py-docutils@0.10:',     type=('build', 'run'))
    depends_on('py-numpy@1.5:',         type=('build', 'run'))
    depends_on('py-quantities@0.10:',   type=('build', 'run'))
    depends_on('py-lazyarray@0.2.9:',   type=('build', 'run'))

    depends_on('py-neo@0.3:0.4.1',      type=('build', 'run'), when="@:0.8.3")
    depends_on('py-neo@0.5.0:',         type=('build', 'run'), when="@0.9.0:")

    depends_on('py-mock@1.0:', type='test')
