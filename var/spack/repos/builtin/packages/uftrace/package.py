# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack import *


class Uftrace(AutotoolsPackage):
    """Dynamic function graph tracer for Linux which demangles C, C++ and Rust calls"""

    homepage = 'https://uftrace.github.io/slide/'
    url      = 'https://github.com/namhyung/uftrace/archive/v0.11.tar.gz'
    git      = 'https://github.com/namhyung/uftrace.git'
    executables = ['^uftrace$']
    maintainers = ['bernhardkaindl']
    tags        = ['trace-tools']

    # The build process uses 'git describe --tags' to get the package version
    version('master', branch='master', get_full_repo=True)
    version('0.11', sha256='101dbb13cb3320ee76525ec26426f2aa1de4e3ee5af74f79cb403ae4d2c6c871')
    version('0.10', sha256='b8b56d540ea95c3eafe56440d6a998e0a140d53ca2584916b6ca82702795bbd9')
    variant("doc", default=False, description="Build uftrace's documentation")
    variant("python2", default=False, description="Build uftrace with python2 support")
    variant("python3", default=True, description="Build uftrace with python3 support")

    depends_on('pandoc', when="+doc", type='build')
    depends_on('capstone')
    depends_on('elfutils')
    depends_on('lsof', type='test')
    depends_on('pkgconfig', type='build')
    depends_on('libunwind')
    depends_on('ncurses')
    depends_on('python@2.7:', when='+python2')
    depends_on('python@3.5:', when='+python3')
    depends_on('lua-luajit')

    # Fix the version string if building below another git repo. Submitted upstream:
    @when('@:0.11')
    def patch(self):
        filter_file('shell git', 'shell test -e .git && git', 'Makefile')

    def check(self):
        make('test', *['V=1', '-j{0}'.format(max(int(make_jobs), 20))])
        # In certain cases, tests using TCP/IP can hang. Ensure that spack can continue:
        os.system("kill -9 `lsof -t ./uftrace` 2>/dev/null")

    def install(self, spec, prefix):
        make('install', *['V=1'])

    def installcheck(self):
        pass

    def test(self):
        """Perform stand-alone/smoke tests using the installed package."""
        uftrace = self.prefix.bin.uftrace
        self.run_test(uftrace,
                      ['-A', '.', '-R', '.', '-P', 'main', uftrace, '-V'],
                      [r'dwarf',
                       r'luajit',
                       r'tui',
                       r'sched',
                       r'dynamic',
                       r'main\(2, ',
                       r'  getopt_long\(2, ',
                       r'  .*printf.*\(',
                       r'} = 0; /\* main \*/'], installed=True,
                      purpose='test: testing the installation')

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'uftrace v(\S+)', output)
        return match.group(1) if match else 'None'
