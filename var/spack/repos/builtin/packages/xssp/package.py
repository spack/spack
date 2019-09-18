# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xssp(AutotoolsPackage):
    """The source code for building the mkdssp, mkhssp, hsspconv, and hsspsoap
       programs is bundled in the xssp project"""

    homepage = "https://github.com/cmbi/xssp"
    url      = "https://github.com/cmbi/xssp/archive/3.0.10.tar.gz"

    version('3.0.10', '01df63c3672eec95662651da45f8c29e')
    version('3.0.9',  '5e47e531095c874f665b83a0a05e8e87')
    version('3.0.8',  '2f95aa39977a4675c7a2810c8d55a2e0')
    version('3.0.7',  '1fe4357628a493664cd67d6b87f701c1')
    version('3.0.6',  '80e3bb3ffb0e6e675e6ecc2a4226b03b')
    version('3.0.5',  '1da38d5a8119c50d49045dab211ee391')
    version('3.0.4',  '92d7fe70a1086d33220959e846ff7052')
    version('3.0.3',  '96632417270259b0549348dfead1fd0d')
    version('3.0.2',  '5a06fb81d7c1ed3d64b79f2cc0f78bb9')
    version('3.0.1',  '2a347ea8ed91583d01026e44035950de')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('boost@1.48:')

    def configure_args(self):
        args = [
            "--with-boost=%s" % self.spec['boost'].prefix]
        return args

    @run_after('configure')
    def edit(self):
        makefile = FileFilter(join_path(self.stage.source_path, 'Makefile'))
        makefile.filter('.*-Werror .*', '                    -Wno-error \\')
