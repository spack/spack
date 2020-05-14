# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
import sys
import os
from spack import *


class Namd(MakefilePackage):
    """NAMDis a parallel molecular dynamics code designed for
    high-performance simulation of large biomolecular systems."""

    homepage = "http://www.ks.uiuc.edu/Research/namd/"
    url      = "file://{0}/NAMD_2.12_Source.tar.gz".format(os.getcwd())
    git      = "https://charm.cs.illinois.edu/gerrit/namd.git"
    manual_download = True

    version("develop", branch="master")
    version('2.14b1', sha256='9407e54f5271b3d3039a5a9d2eae63c7e108ce31b7481e2197c19e1125b43919')
    version('2.13', '9e3323ed856e36e34d5c17a7b0341e38')
    version('2.12', '2a1191909b1ab03bf0205971ad4d8ee9')

    variant('fftw', default='3', values=('none', '2', '3', 'mkl'),
            description='Enable the use of FFTW/FFTW3/MKL FFT')

    variant('interface', default='none', values=('none', 'tcl', 'python'),
            description='Enables TCL and/or python interface')

    depends_on('charmpp@6.10.1:', when="@2.14b1:")
    depends_on('charmpp@6.8.2', when="@2.13")
    depends_on('charmpp@6.7.1', when="@2.12")

    depends_on('fftw@:2.99', when="fftw=2")
    depends_on('fftw@3:', when="fftw=3")

    depends_on('intel-mkl', when="fftw=mkl")

    depends_on('tcl', when='interface=tcl')

    depends_on('tcl', when='interface=python')
    depends_on('python', when='interface=python')

    def _copy_arch_file(self, lib):
        config_filename = 'arch/{0}.{1}'.format(self.arch, lib)
        copy('arch/Linux-x86_64.{0}'.format(lib),
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

    @property
    def arch(self):
        plat = sys.platform
        if plat.startswith("linux"):
            plat = "linux"
        march = platform.machine()
        return '{0}-{1}'.format(plat, march)

    @property
    def build_directory(self):
        return '{0}-spack'.format(self.arch)

    def edit(self, spec, prefix):
        m64 = '-m64 ' if not spec.satisfies('arch=aarch64:') else ''
        with working_dir('arch'):
            with open('{0}.arch'.format(self.build_directory), 'w') as fh:
                # this options are take from the default provided
                # configuration files
                # https://github.com/UIUC-PPL/charm/pull/2778
                if self.spec.satisfies('^charmpp@:6.10.1'):
                    optims_opts = {
                        'gcc': m64 + '-O3 -fexpensive-optimizations \
                                -ffast-math -lpthread',
                        'intel': '-O2 -ip'}
                else:
                    optims_opts = {
                        'gcc': m64 + '-O3 -fexpensive-optimizations \
                                -ffast-math',
                        'intel': '-O2 -ip'}

                optim_opts = optims_opts[self.compiler.name] \
                    if self.compiler.name in optims_opts else ''

                fh.write('\n'.join([
                    'NAMD_ARCH = {0}'.format(self.arch),
                    'CHARMARCH = {0}'.format(self.spec['charmpp'].charmarch),
                    'CXX = {0.cxx} {0.cxx11_flag}'.format(
                        self.compiler),
                    'CXXOPTS = {0}'.format(optim_opts),
                    'CC = {0}'.format(self.compiler.cc),
                    'COPTS = {0}'.format(optim_opts),
                    ''
                ]))

        self._copy_arch_file('base')

        opts = ['--charm-base', spec['charmpp'].prefix]
        fftw_version = spec.variants['fftw'].value
        if fftw_version == 'none':
            opts.append('--without-fftw')
        elif fftw_version == 'mkl':
            self._append_option(opts, 'mkl')
        else:
            _fftw = 'fftw{0}'.format('' if fftw_version == '2' else '3')

            self._copy_arch_file(_fftw)
            opts.extend(['--with-{0}'.format(_fftw),
                         '--fftw-prefix', spec['fftw'].prefix])

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

        config(self.build_directory, *opts)

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.bin)
            install('namd2', prefix.bin)

            # I'm not sure this is a good idea or if an autoload of the charm
            # module would not be better.
            install('charmrun', prefix.bin)
