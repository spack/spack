# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySip(Package):
    """SIP is a tool that makes it very easy to create Python bindings for C
       and C++ libraries."""

    homepage = "https://www.riverbankcomputing.com/software/sip/intro"
    url      = "https://www.riverbankcomputing.com/static/Downloads/sip/4.19.18/sip-4.19.18.tar.gz"
    list_url = "https://www.riverbankcomputing.com/software/sip/download"
    hg       = "https://www.riverbankcomputing.com/hg/sip"

    version('develop', hg=hg)  # wasn't actually able to clone this
    version('4.19.18', sha256='c0bd863800ed9b15dcad477c4017cdb73fa805c25908b0240564add74d697e1e')
    version('4.19.13', sha256='e353a7056599bf5fbd5d3ff9842a6ab2ea3cf4e0304a0f925ec5862907c0d15e')
    version('4.16.7', '32abc003980599d33ffd789734de4c36')
    version('4.16.5', '6d01ea966a53e4c7ae5c5e48c40e49e5')

    variant('module', default='sip', description='Name of private SIP module',
            values=str, multi=False)

    extends('python')

    depends_on('flex', type='build', when='@develop')
    depends_on('bison', type='build', when='@develop')

    # https://www.riverbankcomputing.com/static/Docs/sip/installation.html
    phases = ['configure', 'build', 'install']

    @run_before('configure')
    def prepare(self):
        if self.spec.satisfies('@develop'):
            python('build.py', 'prepare')

    def configure(self, spec, prefix):
        args = [
            '--sip-module={0}'.format(spec.variants['module'].value),
            '--bindir={0}'.format(prefix.bin),
            '--destdir={0}'.format(site_packages_dir),
            '--incdir={0}'.format(python_include_dir),
            '--sipdir={0}'.format(prefix.share.sip),
            '--stubsdir={0}'.format(site_packages_dir),
        ]

        python('configure.py', *args)

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make('install')
