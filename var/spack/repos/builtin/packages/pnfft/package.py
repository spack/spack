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


class Pnfft(AutotoolsPackage):
    """PNFFT is a parallel software library for the calculation of
       three-dimensional nonequispaced FFTs."""

    homepage = "https://www-user.tu-chemnitz.de/~potts/workgroup/pippig/software.php.en"
    url = "https://www-user.tu-chemnitz.de/~potts/workgroup/pippig/software/pnfft-1.0.7-alpha.tar.gz"

    version('1.0.7-alpha', '5caa7f214eed99de2281043ca2367e9e')

    depends_on('pfft')
    depends_on('gsl')

    def configure(self, spec, prefix):
        options = ['--prefix={0}'.format(prefix)]
        if not self.compiler.f77 or not self.compiler.fc:
            options.append("--disable-fortran")

        configure = Executable('../configure')

        if '+double' in spec['fftw']:
            with working_dir('double', create=True):
                configure(*options)
        if '+float' in spec['fftw']:
            with working_dir('float', create=True):
                configure('--enable-float', *options)
        if '+long_double' in spec['fftw']:
            with working_dir('long-double', create=True):
                configure('--enable-long-double', *options)

    def build(self, spec, prefix):
        if '+double' in spec['fftw']:
            with working_dir('double'):
                make()
        if '+float' in spec['fftw']:
            with working_dir('float'):
                make()
        if '+long_double' in spec['fftw']:
            with working_dir('long-double'):
                make()

    def check(self):
        spec = self.spec
        if '+double' in spec['fftw']:
            with working_dir('double'):
                make("check")
        if '+float' in spec['fftw']:
            with working_dir('float'):
                make("check")
        if '+long_double' in spec['fftw']:
            with working_dir('long-double'):
                make("check")

    def install(self, spec, prefix):
        if '+double' in spec['fftw']:
            with working_dir('double'):
                make("install")
        if '+float' in spec['fftw']:
            with working_dir('float'):
                make("install")
        if '+long_double' in spec['fftw']:
            with working_dir('long-double'):
                make("install")
