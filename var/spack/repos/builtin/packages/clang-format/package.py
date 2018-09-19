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
import os
import glob


class ClangFormat(CMakePackage):
    """clang-format formats C, C++, Obj-C, Java, JavaScript, TypeScript code"""

    homepage = "https://clang.llvm.org/"
    url      = "https::/clang.llvm.org/docs/ClangFormat.html"

    # Build dependency
    depends_on('cmake@3.4.3:', type='build')

    # Universal dependency
    depends_on('python@2.7:2.8', when='@:4.999')
    depends_on('python')
    depends_on('py-lit', type=('build', 'run'))

    base_url = 'http://llvm.org/releases/%%(version)s/%(pkg)s-%%(version)s.src.tar.xz'
    llvm_url = base_url % {'pkg': 'llvm'}

    resources = {
        'libcxx': {
            'url': base_url % {'pkg': 'libcxx'},
            'destination': 'projects',
            'placement': 'libcxx',
        },
        'cfe': {
            'url': base_url % {'pkg': 'cfe'},
            'destination': 'tools',
            'placement': 'clang'
        },
    }

    releases = [
        {
            'version': 'trunk',
            'repo': 'http://llvm.org/svn/llvm-project/llvm/trunk',
            'resources': {
                'libcxx': 'http://llvm.org/svn/llvm-project/libcxx/trunk',
                'cfe': 'http://llvm.org/svn/llvm-project/cfe/trunk',
            }
        },
        {
            'version': '6.0.1',
            'md5': 'c88c98709300ce2c285391f387fecce0',
            'resources': {
                'libcxx': '2c13cd0136ab6f8060a4cde85b5f86e2',
                'cfe': '4e419bd4e3b55aa06d872320f754bd85',
            }
        },
        {
            'version': '6.0.0',
            'md5': '788a11a35fa62eb008019b37187d09d2',
            'resources': {
                'libcxx': '4ecad7dfd8ea636205d3ffef028df73a',
                'cfe': '121b3896cb0c7765d690acc5d9495d24',
            }
        },
        {
            'version': '5.0.1',
            'md5': '3a4ec6dcbc71579eeaec7cb157fe2168',
            'resources': {
                'libcxx': 'a9dd49822f2c82cef9a9240d1714a67c',
                'cfe': 'e4daa278d8f252585ab73d196484bf11',
            }
        },
        {
            'version': '5.0.0',
            'md5': '5ce9c5ad55243347ea0fdb4c16754be0',
            'resources': {
                'libcxx': 'a39241a3c9b4d2b7ce1246b9f527b400',
                'cfe': '699c448c6d6d0edb693c87beb1cc8c6e',
            }
        },
        {
            'version': '4.0.1',
            'md5': 'a818e70321b91e2bb2d47e60edd5408f',
            'resources': {
                'libcxx': 'c54f7938e2f393a2cead0af37ed99dfb',
                'cfe': 'a6c7b3e953f8b93e252af5917df7db97',
                }
        },
        {
            'version': '4.0.0',
            'md5': 'ea9139a604be702454f6acf160b4f3a2',
            'resources': {
                'libcxx': '4cf7df466e6f803ec4611ee410ff6781',
                'cfe': '756e17349fdc708c62974b883bf72d37',
            }
        },
        {
            'version': '3.9.1',
            'md5': '3259018a7437e157f3642df80f1983ea',
            'resources': {
                'libcxx': '75a3214224301fc543fa6a38bdf7efe0',
                'cfe': '45713ec5c417ed9cad614cd283d786a1',
            }
        },
        {
            'version': '3.9.0',
            'md5': 'f2093e98060532449eb7d2fcfd0bc6c6',
            'resources': {
                'libcxx': '0a11efefd864ce6f321194e441f7e569',
                'cfe': '29e1d86bee422ab5345f5e9fb808d2dc',
            }
        },
        {
            'version': '3.8.1',
            'md5': '538467e6028bbc9259b1e6e015d25845',
            'resources': {
                'libcxx': '1bc60150302ff76a0d79d6f9db22332e',
                'cfe': '4ff2f8844a786edb0220f490f7896080',
            }
        },
        {
            'version': '3.8.0',
            'md5': '07a7a74f3c6bd65de4702bf941b511a0',
            'resources': {
                'libcxx': 'd6e0bdbbee39f7907ad74fd56d03b88a',
                'cfe': 'cc99e7019bb74e6459e80863606250c5',
            }
        },
        {
            'version': '3.7.1',
            'md5': 'bf8b3a2c79e61212c5409041dfdbd319',
            'resources': {
                'libcxx': 'f9c43fa552a10e14ff53b94d04bea140',
                'cfe': '0acd026b5529164197563d135a8fd83e',
            }
        },
        {
            'version': '3.7.0',
            'md5': 'b98b9495e5655a672d6cb83e1a180f8e',
            'resources': {
                'libcxx': '46aa5175cbe1ad42d6e9c995968e56dd',
                'cfe': '8f9d27335e7331cf0a4711e952f21f01',
            }
        },
        {
            'version': '3.6.2',
            'md5': '0c1ee3597d75280dee603bae9cbf5cc2',
            'resources': {
                'libcxx': '22214c90697636ef960a49aef7c1823a',
                'cfe': 'ff862793682f714bb7862325b9c06e20',
            }
        },
        {
            'version': '3.5.1',
            'md5': '2d3d8004f38852aa679e5945b8ce0b14',
            'resources': {
                'libcxx': '406f09b1dab529f3f7879f4d548329d2',
                'cfe': '93f9532f8f7e6f1d8e5c1116907051cb',
            }
        },
    ]

    for release in releases:
        if release['version'] == 'trunk':
            version(release['version'], svn=release['repo'])

            for name, repo in release['resources'].items():
                resource(name=name,
                         svn=repo,
                         destination=resources[name]['destination'],
                         when='@%s%s' % (release['version'],
                                         resources[name].get('variant', "")),
                         placement=resources[name].get('placement', None))
        else:
            version(release['version'], release['md5'], url=llvm_url % release)

            for name, md5 in release['resources'].items():
                resource(name=name,
                         url=resources[name]['url'] % release,
                         md5=md5,
                         destination=resources[name]['destination'],
                         when='@%s%s' % (release['version'],
                                         resources[name].get('variant', "")),
                         placement=resources[name].get('placement', None))

    # Rather than execute the default build target, only build clang-format
    build_targets = ['clang-format']

    def cmake_args(self):
        spec = self.spec

        cmake_args = [
            '-DLLVM_ENABLE_LIBCXX=ON',
            '-DPYTHON_EXECUTABLE:PATH={0}'.format(spec['python'].command.path),
        ]

        if spec.satisfies('@3.9.0:'):
            cmake_args.append('-DCLANG_DEFAULT_CXX_STDLIB=libc++')

        if spec.satisfies('@4.0.0:') and spec.satisfies('platform=linux'):
            cmake_args.append('-DCMAKE_BUILD_WITH_INSTALL_RPATH=1')
        return cmake_args

    # Override the install target because we do not want to run
    # `cmake --build . --target install`; rather, we only want to install
    # files that are part of clang-format
    def install(self, spec, prefix):
        mkdirp(self.spec.prefix.bin)
        clang_format_path = 'spack-build/bin/clang-format'
        install(clang_format_path,
                join_path(self.spec.prefix.bin, 'clang-format'))
        tools_path = 'tools/clang/tools/clang-format'
        install(join_path(tools_path, 'git-clang-format'),
                join_path(self.spec.prefix.bin, 'git-clang-format'))

        mkdirp(self.spec.prefix.share)
        for f in glob.glob(join_path(tools_path, 'clang-format*')):
            install(f,
                    join_path(self.spec.prefix.share, os.path.basename(f)))
