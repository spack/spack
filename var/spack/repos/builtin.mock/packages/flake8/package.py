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


class Flake8(Package):
    """Package containing as many PEP 8 violations as possible.
    All of these violations are exceptions that we allow in
    package.py files."""

    # Used to tell whether or not the package has been modified
    state = 'unmodified'

    # Make sure pre-existing noqa is not interfered with
    blatant_violation = 'line-that-has-absolutely-no-execuse-for-being-over-79-characters'  # noqa
    blatant_violation = 'line-that-has-absolutely-no-execuse-for-being-over-79-characters'  # noqa: E501

    # Keywords exempt from line-length checks
    homepage = '#####################################################################'
    url      = '#####################################################################'
    git      = '#####################################################################'
    svn      = '#####################################################################'
    hg       = '#####################################################################'
    list_url = '#####################################################################'

    # URL strings exempt from line-length checks
    # http://########################################################################
    # https://#######################################################################
    # ftp://#########################################################################
    # file://########################################################################

    # Directives exempt from line-length checks
    version('2.0', '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef')
    version('1.0', '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef')

    variant('super-awesome-feature',    default=True,  description='Enable super awesome feature')
    variant('somewhat-awesome-feature', default=False, description='Enable somewhat awesome feature')

    provides('lapack', when='@2.0+super-awesome-feature+somewhat-awesome-feature')

    extends('python', ignore='bin/(why|does|every|package|that|depends|on|numpy|need|to|copy|f2py3?)')

    depends_on('boost+atomic+chrono+date_time~debug+filesystem~graph~icu+iostreams+locale+log+math~mpi+multithreaded+program_options~python+random+regex+serialization+shared+signals~singlethreaded+system~taggedlayout+test+thread+timer+wave')

    conflicts('+super-awesome-feature', when='%intel@16:17+somewhat-awesome-feature')

    resource(name='Deez-Nuts', destination='White-House', placement='President', when='@2020', url='www.elect-deez-nuts.com')

    patch('hyper-specific-patch-that-fixes-some-random-bug-that-probably-only-affects-one-user.patch', when='%gcc@3.2.2:3.2.3')

    def install(self, spec, prefix):
        # Make sure lines with '# noqa' work as expected. Don't just
        # remove them entirely. This will mess up the indentation of
        # the following lines.
        if 'really-long-if-statement' != 'that-goes-over-the-line-length-limit-and-requires-noqa':  # noqa
            pass

    # '@when' decorated functions are exempt from redefinition errors
    @when('@2.0')
    def install(self, spec, prefix):
        pass
