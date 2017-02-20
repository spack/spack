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
import os

from spack import *


class Llvm(Package):
    """The LLVM Project is a collection of modular and reusable compiler and
       toolchain technologies. Despite its name, LLVM has little to do
       with traditional virtual machines, though it does provide helpful
       libraries that can be used to build them. The name "LLVM" itself
       is not an acronym; it is the full name of the project.
    """

    homepage = 'http://llvm.org/'
    url = 'http://llvm.org/releases/3.7.1/llvm-3.7.1.src.tar.xz'

    family = 'compiler'  # Used by lmod

    # currently required by mesa package
    version('3.0', 'a8e5f5f1c1adebae7b4a654c376a6005',
            url='http://llvm.org/releases/3.0/llvm-3.0.tar.gz')

    variant('debug', default=False,
            description="Build a debug version of LLVM, this increases "
            "binary size by an order of magnitude, make sure you have "
            "20-30gb of space available to build this")
    variant('clang', default=True,
            description="Build the LLVM C/C++/Objective-C compiler frontend")
    variant('lldb', default=True, description="Build the LLVM debugger")
    variant('internal_unwind', default=True,
            description="Build the libcxxabi libunwind")
    variant('polly', default=True,
            description="Build the LLVM polyhedral optimization plugin, "
            "only builds for 3.7.0+")
    variant('libcxx', default=True,
            description="Build the LLVM C++ standard library")
    variant('compiler-rt', default=True,
            description="Build LLVM compiler runtime, including sanitizers")
    variant('gold', default=True,
            description="Add support for LTO with the gold linker plugin")
    variant('shared_libs', default=False,
            description="Build all components as shared libraries, faster, "
            "less memory to build, less stable")
    variant('link_dylib', default=False,
            description="Build and link the libLLVM shared library rather "
            "than static")
    variant('all_targets', default=True,
            description="Build all supported targets, default targets "
            "<current arch>,NVPTX,AMDGPU,CppBackend")

    # Build dependency
    depends_on('cmake@2.8.12.2:', type='build')

    # Universal dependency
    depends_on('python@2.7:2.8')  # Seems not to support python 3.X.Y
    depends_on('py-lit')

    # lldb dependencies
    depends_on('ncurses', when='+lldb')
    depends_on('swig', when='+lldb')
    depends_on('libedit', when='+lldb')

    # gold support
    depends_on('binutils+gold', when='+gold')

    # polly plugin
    depends_on('gmp', when='@:3.6.999 +polly')
    depends_on('isl', when='@:3.6.999 +polly')

    base_url = 'http://llvm.org/releases/%%(version)s/%(pkg)s-%%(version)s.src.tar.xz'
    llvm_url = base_url % {'pkg': 'llvm'}

    resources = {
        'compiler-rt': {
            'url': base_url % {'pkg': 'compiler-rt'},
            'destination': 'projects',
            'placement': 'compiler-rt',
            'variant': '+compiler-rt',
        },
        'openmp': {
            'url': base_url % {'pkg': 'openmp'},
            'destination': 'projects',
            'placement': 'openmp',
            'variant': '+clang',
        },
        'libcxx': {
            'url': base_url % {'pkg': 'libcxx'},
            'destination': 'projects',
            'placement': 'libcxx',
            'variant': '+libcxx',
        },
        'libcxxabi': {
            'url':  base_url % {'pkg': 'libcxxabi'},
            'destination': 'projects',
            'placement': 'libcxxabi',
            'variant': '+libcxx',
        },
        'cfe': {
            'url':  base_url % {'pkg': 'cfe'},
            'destination': 'tools',
            'placement': 'clang',
            'variant': '+clang',
        },
        'clang-tools-extra': {
            'url':  base_url % {'pkg': 'clang-tools-extra'},
            'destination': 'tools/clang/tools',
            'placement': 'extra',
            'variant': '+clang',
        },
        'lldb': {
            'url':  base_url % {'pkg': 'lldb'},
            'destination': 'tools',
            'placement': 'lldb',
            'variant': '+lldb',
        },
        'polly': {
            'url':  base_url % {'pkg': 'polly'},
            'destination': 'tools',
            'placement': 'polly',
            'variant': '+polly',
        },
        'libunwind': {
            'url':  base_url % {'pkg': 'libunwind'},
            'destination': 'projects',
            'placement': 'libunwind',
            'variant': '+internal_unwind',
        },
    }
    releases = [
        {
            'version': 'trunk',
            'repo': 'http://llvm.org/svn/llvm-project/llvm/trunk',
            'resources': {
                'compiler-rt': 'http://llvm.org/svn/llvm-project/compiler-rt/trunk',
                'openmp': 'http://llvm.org/svn/llvm-project/openmp/trunk',
                'polly': 'http://llvm.org/svn/llvm-project/polly/trunk',
                'libcxx': 'http://llvm.org/svn/llvm-project/libcxx/trunk',
                'libcxxabi': 'http://llvm.org/svn/llvm-project/libcxxabi/trunk',
                'cfe': 'http://llvm.org/svn/llvm-project/cfe/trunk',
                'clang-tools-extra': 'http://llvm.org/svn/llvm-project/clang-tools-extra/trunk',
                'lldb': 'http://llvm.org/svn/llvm-project/lldb/trunk',
                'libunwind': 'http://llvm.org/svn/llvm-project/libunwind/trunk',
                }
            },
            {
                'version': '3.9.1',
                'md5': '3259018a7437e157f3642df80f1983ea',
                'resources': {
                    'compiler-rt': 'aadc76e7e180fafb10fb729444e287a3',
                    'openmp': 'f076916bf2f49229b4df9fa0bb002599',
                    'polly': '2cc7fe2bd9539775ba140abfd375bec6',
                    'libcxx': '75a3214224301fc543fa6a38bdf7efe0',
                    'libcxxabi': '62fd584b38cc502172c2ffab041b5fcc',
                    'cfe': '45713ec5c417ed9cad614cd283d786a1',
                    'clang-tools-extra': '1a01d545a064fcbc46a2f05f6880d3d7',
                    'lldb': '91399402f287d3f637db1207113deecb',
                    'libunwind': 'f273dd0ed638ad0601b23176a36f187b',
                    }
                },
            {
                'version': '3.9.0',
                'md5': 'f2093e98060532449eb7d2fcfd0bc6c6',
                'resources': {
                    'compiler-rt': 'b7ea34c9d744da16ffc0217b6990d095',
                    'openmp': '5390164f2374e1444e82393541ecf6c7',
                    'polly': '1cf328cbae25267749b68cfa6f113674',
                    'libcxx': '0a11efefd864ce6f321194e441f7e569',
                    'libcxxabi': 'd02642308e22e614af6b061b9b4fedfa',
                    'cfe': '29e1d86bee422ab5345f5e9fb808d2dc',
                    'clang-tools-extra': 'f4f663068c77fc742113211841e94d5e',
                    'lldb': '968d053c3c3d7297983589164c6999e9',
                    'libunwind': '3e5c87c723a456be599727a444b1c166',
                    }
                },
            {
                'version': '3.8.1',
                'md5': '538467e6028bbc9259b1e6e015d25845',
                'resources': {
                    'compiler-rt': 'f140db073d2453f854fbe01cc46f3110',
                    'openmp': '078b8d4c51ad437a4f8b5989f5ec4156',
                    'polly': '8a40e697a4ba1c8b640b85d074bd6e25',
                    'libcxx': '1bc60150302ff76a0d79d6f9db22332e',
                    'libcxxabi': '3c63b03ba2f30a01279ca63384a67773',
                    'cfe': '4ff2f8844a786edb0220f490f7896080',
                    'clang-tools-extra': '6e49f285d0b366cc3cab782d8c92d382',
                    'lldb': '9e4787b71be8e432fffd31e13ac87623',
                    'libunwind': 'd66e2387e1d37a8a0c8fe6a0063a3bab',
                    }
                },
            {
                'version': '3.8.0',
                'md5': '07a7a74f3c6bd65de4702bf941b511a0',
                'resources': {
                    'compiler-rt': 'd6fcbe14352ffb708e4d1ac2e48bb025',
                    'openmp': '8fd7cc35d48051613cf1e750e9f22e40',
                    'polly': '1b3b20f52d34a4024e21a4ea7112caa7',
                    'libcxx': 'd6e0bdbbee39f7907ad74fd56d03b88a',
                    'libcxxabi': 'bbe6b4d72c7c5978550d370af529bcf7',
                    'cfe': 'cc99e7019bb74e6459e80863606250c5',
                    'clang-tools-extra': 'c2344f50e0eea0b402f0092a80ddc036',
                    'lldb': 'a5da35ed9cc8c8817ee854e3dbfba00e',
                    'libunwind': '162ade468607f153cca12be90b5194fa',
                    }
                },
            {
                'version': '3.7.1',
                'md5': 'bf8b3a2c79e61212c5409041dfdbd319',
                'resources': {
                    'compiler-rt': '1c6975daf30bb3b0473b53c3a1a6ff01',
                    'openmp': 'b4ad08cda4e5c22e42b66062b140438e',
                    'polly': '3a2a7367002740881637f4d47bca4dc3',
                    'libcxx': 'f9c43fa552a10e14ff53b94d04bea140',
                    'libcxxabi': '52d925afac9f97e9dcac90745255c169',
                    'cfe': '0acd026b5529164197563d135a8fd83e',
                    'clang-tools-extra': '5d49ff745037f061a7c86aeb6a24c3d2',
                    'lldb': 'a106d8a0d21fc84d76953822fbaf3398',
                    'libunwind': '814bd52c9247c5d04629658fbcb3ab8c',
                    }
                },
            {
                'version': '3.7.0',
                'md5': 'b98b9495e5655a672d6cb83e1a180f8e',
                'resources': {
                    'compiler-rt': '383c10affd513026f08936b5525523f5',
                    'openmp': 'f482c86fdead50ba246a1a2b0bbf206f',
                    'polly': '32f93ffc9cc7e042df22089761558f8b',
                    'libcxx': '46aa5175cbe1ad42d6e9c995968e56dd',
                    'libcxxabi': '5aa769e2fca79fa5335cfae8f6258772',
                    'cfe': '8f9d27335e7331cf0a4711e952f21f01',
                    'clang-tools-extra': 'd5a87dacb65d981a427a536f6964642e',
                    'lldb': 'e5931740400d1dc3e7db4c7ba2ceff68',
                    'libunwind': '9a75392eb7eb8ed5c0840007e212baf5',
                    }
                },
        {
            'version': '3.6.2',
            'md5': '0c1ee3597d75280dee603bae9cbf5cc2',
            'resources': {
                'compiler-rt': 'e3bc4eb7ba8c39a6fe90d6c988927f3c',
                'openmp': '65dd5863b9b270960a96817e9152b123',
                'libcxx': '22214c90697636ef960a49aef7c1823a',
                'libcxxabi': '17518e361e4e228f193dd91e8ef54ba2',
                'cfe': 'ff862793682f714bb7862325b9c06e20',
                'clang-tools-extra': '3ebc1dc41659fcec3db1b47d81575e06',
                'lldb': '51e5eb552f777b950bb0ff326e60d5f0',
            }
        },
        {
            'version': '3.5.1',
            'md5': '2d3d8004f38852aa679e5945b8ce0b14',
            'resources': {
                'compiler-rt': 'd626cfb8a9712cb92b820798ab5bc1f8',
                'openmp': '121ddb10167d7fc38b1f7e4b029cf059',
                'libcxx': '406f09b1dab529f3f7879f4d548329d2',
                'libcxxabi': 'b22c707e8d474a99865ad3c521c3d464',
                'cfe': '93f9532f8f7e6f1d8e5c1116907051cb',
                'clang-tools-extra': 'f13f31ed3038acadc6fa63fef812a246',
                'lldb': 'cc5ea8a414c62c33e760517f8929a204',
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

    def install(self, spec, prefix):
        env['CXXFLAGS'] = self.compiler.cxx11_flag
        cmake_args = [arg for arg in std_cmake_args if 'BUILD_TYPE' not in arg]

        build_type = 'RelWithDebInfo' if '+debug' in spec else 'Release'
        cmake_args.extend([
            '..',
            '-DCMAKE_BUILD_TYPE=' + build_type,
            '-DLLVM_REQUIRES_RTTI:BOOL=ON',
            '-DCLANG_DEFAULT_OPENMP_RUNTIME:STRING=libomp',
            '-DPYTHON_EXECUTABLE:PATH=%s/bin/python' % spec['python'].prefix])

        if '+gold' in spec:
            cmake_args.append('-DLLVM_BINUTILS_INCDIR=' +
                              os.path.join(spec['binutils'].prefix, 'include'))
        if '+polly' in spec:
            cmake_args.append('-DLINK_POLLY_INTO_TOOLS:Bool=ON')
        else:
            cmake_args.append('-DLLVM_EXTERNAL_POLLY_BUILD:Bool=OFF')

        if '+clang' not in spec:
            cmake_args.append('-DLLVM_EXTERNAL_CLANG_BUILD:Bool=OFF')
        if '+lldb' not in spec:
            cmake_args.append('-DLLVM_EXTERNAL_LLDB_BUILD:Bool=OFF')
        if '+internal_unwind' not in spec:
            cmake_args.append('-DLLVM_EXTERNAL_LIBUNWIND_BUILD:Bool=OFF')
        if '+libcxx' not in spec:
            cmake_args.append('-DLLVM_EXTERNAL_LIBCXX_BUILD:Bool=OFF')
            cmake_args.append('-DLLVM_EXTERNAL_LIBCXXABI_BUILD:Bool=OFF')
        if '+compiler-rt' not in spec:
            cmake_args.append('-DLLVM_EXTERNAL_COMPILER_RT_BUILD:Bool=OFF')

        if '+shared_libs' in spec:
            cmake_args.append('-DBUILD_SHARED_LIBS:Bool=ON')

        if '+link_dylib' in spec:
            cmake_args.append('-DLLVM_LINK_LLVM_DYLIB:Bool=ON')

        if '+all_targets' not in spec:  # all is default on cmake
            targets = ['CppBackend', 'NVPTX', 'AMDGPU']
            if 'x86' in spec.architecture.target.lower():
                targets.append('X86')
            elif 'arm' in spec.architecture.target.lower():
                targets.append('ARM')
            elif 'aarch64' in spec.architecture.target.lower():
                targets.append('AArch64')
            elif 'sparc' in spec.architecture.target.lower():
                targets.append('sparc')
            elif ('ppc' in spec.architecture.target.lower() or
                  'power' in spec.architecture.target.lower()):
                targets.append('PowerPC')

            cmake_args.append(
                '-DLLVM_TARGETS_TO_BUILD:Bool=' + ';'.join(targets))

        if '+clang' not in spec:
            if '+clang_extra' in spec:
                raise SpackException(
                    'The clang_extra variant requires the `+clang` variant.')
            if '+lldb' in spec:
                raise SpackException(
                    'The lldb variant requires the `+clang` variant')

        with working_dir('spack-build', create=True):
            cmake(*cmake_args)
            make()
            make("install")
            cp = which('cp')
            cp('-a', 'bin/', prefix)
