##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import re


class Infer(Package):
    """Infer: a static analyzer for Java, C, C++, and Objective-C

       Infer is a static program analyzer for Java, C, and
       Objective-C, written in OCaml. Infer is deployed within
       Facebook and it is running continuously to verify select
       properties of every code modification for the main Facebook
       apps for Android and iOS, Facebook Messenger, Instagram, and
       other apps. It can be used for other code too: Infer can also
       analyze C code, and Java code that is not Android.  At present
       Infer is tracking problems caused by null pointer dereferences
       and resource and memory leaks, which cause some of the more
       important problems on mobile. """

    homepage = "http://fbinfer.com/"
    url      = "https://github.com/facebook/infer/archive/v0.13.1.tar.gz"

    version('develop', git='https://github.com/facebook/infer', branch='master')
    version('0.13.1', '06867fe94439ecac3f1a9fd202ed5b88')

    depends_on('autoconf', type=('build'))
    depends_on('automake', type=('build'))
    depends_on('cmake', type=('build'))
    depends_on('libtool', type=('build'))
    depends_on('ocaml', type=('build'))
    depends_on('opam', type=('build'))
    depends_on('pkg-config', type=('build'))

    parallel = False

    def setup_environment(self, spack_env, run_env):
        spack_env.set('OPAMYES', '1')
        spack_env.set('INFER_CONFIGURE_OPTS',
                      ('--prefix={0}'.format(self.prefix) +
                       ' --disable-ocaml-binannot' +
                       ' --without-fcp-clang'))

    def install(self, spec, prefix):
        # Install a local version of opam for building Infer. Options
        # taken from
        # https://github.com/Homebrew/homebrew-core/blob/master/Formula/infer.rb
        opamroot = join_path('.', 'opamroot')
        mkdirp(opamroot)
        env['OPAMROOT'] = opamroot
        opam = Executable(join_path(self.spec['opam'].prefix.bin, 'opam'))
        opam('init', '--no-setup')

        # Detect OCaml version used in Infer build scropt
        build_file_path = join_path('.', 'build-infer.sh')
        with open(build_file_path, 'r') as f:
            p = re.compile('OCAML_VERSION=\${OCAML_VERSION:-\"([^\"]+)\"}')
            ocaml_version = p.search(f.read()).group(1)
            ocaml_version_number = ocaml_version.split('+')[0]

        comp_file_path = join_path(opamroot, 'compilers', ocaml_version_number,
                                   ocaml_version, ocaml_version + '.comp')
        comp_file = FileFilter(comp_file_path)

        # Add the same options Homebrew does for the configure step
        configure_string = r'["./configure"'
        configure_no_graph_string = r'["./configure" "-no-graph"'
        comp_file.filter(re.escape(configure_string),
                         configure_no_graph_string)

        # Substitution to ensure `infer --version` reports a release
        # version number; see
        # https://github.com/Homebrew/homebrew-core/blob/master/Formula/infer.rb
        infer_ml_in = join_path('infer', 'src', 'base', 'Version.ml.in')
        infer_file = FileFilter(infer_ml_in)
        is_release_string = 'let is_release = is_yes "@IS_RELEASE_TRUE@"'
        is_release_true_string = 'let is_release = true'
        infer_file.filter(re.escape(is_release_string),
                          re.escape(is_release_true_string))

        # TODO: Add Java support; for now, support for C, C++, and
        # Objective-C is the focus of this package
        target_platform = "clang"

        build_infer = Executable(build_file_path)
        build_infer(target_platform, '--yes')

        opam('config', 'exec',
             '--switch=infer-{0}'.format(ocaml_version), '--', 'make',
             'install')
