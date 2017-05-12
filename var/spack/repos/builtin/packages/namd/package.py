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
import platform
import shutil
import sys
from spack import *


class Namd(MakefilePackage):
    """NAMDis a parallel molecular dynamics code designed for
    high-performance simulation of large biomolecular systems."""

    homepage = "http://www.ks.uiuc.edu/Research/namd/"
    url      = "file://NAMD_2.12_Source.tar.gz"

    version('2.12', '2a1191909b1ab03bf0205971ad4d8ee9')

    variant('fftw', default='3', values=('none', '2', '3', 'mkl'),
            description='Enable the use of FFTW/FFTW3/MKL FFT')

    variant('interface', default='none', values=('none', 'tcl', 'python'),
            description='Enables TCL and/or python interface')

    depends_on('charm')

    depends_on('fftw@:2.99', when="fftw=2")
    depends_on('fftw@3:', when="fftw=3")

    depends_on('fftw@3:', when="fftw=mkl")
    depends_on('intel-mkl', when="fftw=mkl")

    depends_on('tcl', when='interface=tcl')

    depends_on('tcl', when='interface=python')
    depends_on('python', when='interface=python')

    def _copy_arch_file(self, lib):
        config_filename = 'arch/{0}.{1}'.format(self.arch, lib)
        shutil.copy('arch/Linux-x86_64.{0}'.format(lib),
                    config_filename)
        if lib == 'tcl':
            filter_file(r'-ltcl8\.5',
                        '-ltcl{0}'.format(self.spec['tcl'].version.up_to(2)),
                        config_filename)

    def _append_option(self, opts, lib):
        if lib != 'python':
            self._copy_arch_file(lib)
        spec = self.spec
        opts.extend([
            '--with-{0}'.format(lib),
            '--{0}-prefix'.format(lib), spec[lib].prefix
        ])

    def edit(self, spec, prefix):
        plat = sys.platform
        if plat.startswith("linux"):
            plat = "linux"
        march = platform.machine()

        self.arch = '{0}-{1}'.format(plat, march)

        with working_dir('arch'):
            with open('{0}-spack.arch'.format(self.arch), 'w') as fh:
                fh.write('\n'.join([
                    'NAMD_ARCH = {0}'.format(self.arch),
                    'CHARMARCH = ',
                    'CXX = {0.cxx} -m64 {0.cxx11_flag} -O3'.format(
                        self.compiler),
                    'CXXOPTS = -fexpensive-optimizations -ffast-math',
                    'CC = {0} -m64 -O3'.format(self.compiler.cc),
                    'COPTS = -fexpensive-optimizations -ffast-math',
                    ''
                ]))

        self._copy_arch_file('base')

        opts = ['--charm-base', spec['charm'].prefix]
        fftw_version = spec.variants['fftw'].value
        if fftw_version != 'none':
            _fftw = 'fftw{0}'.format('' if fftw_version == '2' else '3')

            self._copy_arch_file(_fftw)
            opts.extend(['--with-{0}'.format(_fftw),
                         '--fftw-prefix', spec['fftw'].prefix])

            if fftw_version == 'mkl':
                self._append_option(opts, 'mkl')
        else:
            opts.append('--without-fftw')

        interface_type = spec.variants['interface'].value
        if interface_type != 'none':
            self._append_option(opts, 'tcl')

            if interface_type == 'python':
                self._append_option(opts, 'python')
        else:
            opts.extend([
                '--without-tcl',
                '--without-python'
            ])

        config = Executable('./config')

        config('{0}-spack'.format(self.arch), *opts)

    def build(self, spec, prefix):
        with working_dir('{0}-spack'.format(self.arch)):
            make()

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir('{0}-spack'.format(self.arch)):
            install('namd2', prefix.bin)

            # I'm not sure this is a good idea or if an autoload of the charm
            # module would not be better.
            install('charmrun', prefix.bin)
