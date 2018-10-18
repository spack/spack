# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Stat(AutotoolsPackage):
    """Library to create, manipulate, and export graphs Graphlib."""

    homepage = "http://paradyn.org/STAT/STAT.html"
    url      = "https://github.com/LLNL/STAT/archive/v2.0.0.tar.gz"
    git      = "https://github.com/llnl/stat.git"

    version('develop', branch='develop')
    version('4.0.0', 'b357160662ced251bc55cb1b884c3407',
            url='https://github.com/LLNL/STAT/releases/download/v4.0.0/stat-4.0.0.tar.gz')
    version('3.0.1', 'dac6f23c3639a0b21f923dc6219ba385',
            url='https://github.com/LLNL/STAT/files/911503/stat-3.0.1.zip')
    version('3.0.0', 'a97cb235c266371c4a26329112de48a2',
            url='https://github.com/LLNL/STAT/releases/download/v3.0.0/STAT-3.0.0.tar.gz')
    version('2.2.0', '26bd69dd57a15afdd5d0ebdb0b7fb6fc')
    version('2.1.0', 'ece26beaf057aa9134d62adcdda1ba91')
    version('2.0.0', 'c7494210b0ba26b577171b92838e1a9b')

    # TODO: dysect requires Dyninst patch for version 3.0.0b
    variant('dysect', default=False, description="enable DySectAPI")
    variant('examples', default=False, description="enable examples")
    variant('fgfs', default=True, description="enable file broadcasting")

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('dyninst', when='~dysect')
    depends_on('dyninst@8.2.1+stat_dysect', when='+dysect')
    depends_on('fast-global-file-status', when='+fgfs')
    depends_on('graphlib@2.0.0', when='@2.0.0:2.2.0')
    depends_on('graphlib@3.0.0', when='@3:')
    depends_on('graphviz', type=('build', 'link', 'run'))
    depends_on('launchmon')
    depends_on('mrnet')
    depends_on('python@:2.8')
    depends_on('py-pygtk', type=('build', 'run'))
    depends_on('py-enum34', type=('run'))
    depends_on('swig')
    depends_on('mpi', when='+examples')

    patch('configure_mpicxx.patch', when='@2.1.0')

    def configure_args(self):
        spec = self.spec
        args = [
            "--with-launchmon=%s"   % spec['launchmon'].prefix,
            "--with-mrnet=%s"       % spec['mrnet'].prefix,
            "--with-graphlib=%s"    % spec['graphlib'].prefix,
            "--with-stackwalker=%s" % spec['dyninst'].prefix,
            "--with-python=%s"      % spec['python'].command.path,
        ]
        if '+fgfs' in spec:
            args.append('--with-fgfs=%s'
                        % spec['fast-global-file-status'].prefix)
        if '+dysect' in spec:
            args.append('--enable-dysectapi')
        if '~examples' in spec:
            args.append('--disable-examples')
        return args
