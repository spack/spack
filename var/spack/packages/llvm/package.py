##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by David Beckingsale, david@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import os, shutil


class Llvm(Package):
    """The LLVM Project is a collection of modular and reusable compiler and
       toolchain technologies. Despite its name, LLVM has little to do with
       traditional virtual machines, though it does provide helpful libraries
       that can be used to build them. The name "LLVM" itself is not an acronym;
       it is the full name of the project.
    """
    homepage = 'http://llvm.org/'
    url = 'http://llvm.org/releases/3.7.0/llvm-3.7.0.src.tar.xz'

    version('3.0', 'a8e5f5f1c1adebae7b4a654c376a6005', url='http://llvm.org/releases/3.0/llvm-3.0.tar.gz') # currently required by mesa package

    variant('debug', default=False, description="Build a debug version of LLVM, this increases binary size by an order of magnitude, make sure you have 20-30gb of space available to build this")
    variant('clang', default=True, description="Build the LLVM C/C++/Objective-C compiler frontend")
    variant('lldb', default=True, description="Build the LLVM debugger")
    variant('internal_unwind', default=True, description="Build the libcxxabi libunwind")
    variant('polly', default=True, description="Build the LLVM polyhedral optimization plugin, only builds for 3.7.0+")
    variant('libcxx', default=True, description="Build the LLVM C++ standard library")
    variant('compiler-rt', default=True, description="Build the LLVM compiler runtime, including sanitizers")
    variant('lto', default=True, description="Add support for LTO with the gold linker plugin")


    # Universal dependency
    depends_on('python@2.7:')

    # lldb dependencies
    depends_on('ncurses', when='+lldb')
    depends_on('swig', when='+lldb')
    depends_on('libedit', when='+lldb')

    # gold support
    depends_on('binutils+gold', when='+lto')

    # polly plugin
    depends_on('gmp', when='+polly')
    depends_on('isl', when='+polly')

    base_url =  'http://llvm.org/releases/%%(version)s/%(pkg)s-%%(version)s.src.tar.xz'
    llvm_url = base_url % { 'pkg' : 'llvm'}

    resources = {
                    'compiler-rt' : {
                        'url' : base_url % { 'pkg' : 'compiler-rt'},
                        'destination' : 'projects',
                        'placement' : 'compiler-rt',
                    },
                    'openmp' : {
                        'url' : base_url % { 'pkg' : 'openmp'},
                        'destination' : 'projects',
                        'placement' : 'openmp',
                    },
                    'libcxx' : {
                        'url' : base_url % { 'pkg' : 'libcxx'},
                        'destination' : 'projects',
                        'placement' : 'libcxx',
                    },
                    'libcxxabi' : {
                        'url' :  base_url % { 'pkg' : 'libcxxabi'},
                        'destination' : 'projects',
                        'placement' : 'libcxxabi',
                    },
                    'clang' : {
                        'url' :  base_url % { 'pkg' : 'cfe'},
                        'destination' : 'tools',
                        'placement' : 'clang',
                    },
                    'clang-tools-extra' : {
                        'url' :  base_url % { 'pkg' : 'clang-tools-extra'},
                        'destination' : 'tools/clang/tools',
                        'placement' : 'extra',
                    },
                    'lldb' : {
                        'url' :  base_url % { 'pkg' : 'lldb'},
                        'destination' : 'tools',
                        'placement' : 'lldb',
                    },
                    'polly' : {
                        'url' :  base_url % { 'pkg' : 'polly'},
                        'destination' : 'tools',
                        'placement' : 'polly',
                    },
                    'llvm-libunwind' : {
                        'url' :  base_url % { 'pkg' : 'libunwind'},
                        'destination' : 'projects',
                        'placement' : 'libunwind',
                    },
                }
    releases = [
                  {
                    'version' : '3.7.0',
                    'md5':'b98b9495e5655a672d6cb83e1a180f8e',
                    'resources' : {
                        'compiler-rt' : '383c10affd513026f08936b5525523f5',
                        'openmp' : 'f482c86fdead50ba246a1a2b0bbf206f',
                        'polly' : '32f93ffc9cc7e042df22089761558f8b',
                        'libcxx' : '46aa5175cbe1ad42d6e9c995968e56dd',
                        'libcxxabi' : '5aa769e2fca79fa5335cfae8f6258772',
                        'clang' : '8f9d27335e7331cf0a4711e952f21f01',
                        'clang-tools-extra' : 'd5a87dacb65d981a427a536f6964642e',
                        'lldb' : 'e5931740400d1dc3e7db4c7ba2ceff68',
                        'llvm-libunwind' : '9a75392eb7eb8ed5c0840007e212baf5',
                        }
                  },
                  {
                    'version' : '3.6.2',
                    'md5':'0c1ee3597d75280dee603bae9cbf5cc2',
                    'resources' : {
                        'compiler-rt' : 'e3bc4eb7ba8c39a6fe90d6c988927f3c',
                        'openmp' : '65dd5863b9b270960a96817e9152b123',
                        'libcxx' : '22214c90697636ef960a49aef7c1823a',
                        'libcxxabi' : '17518e361e4e228f193dd91e8ef54ba2',
                        'clang' : 'ff862793682f714bb7862325b9c06e20',
                        'clang-tools-extra' : '3ebc1dc41659fcec3db1b47d81575e06',
                        'lldb' : '51e5eb552f777b950bb0ff326e60d5f0',
                        }
                  },
                  {
                    'version' : '3.5.1',
                    'md5':'2d3d8004f38852aa679e5945b8ce0b14',
                    'resources' : {
                        'compiler-rt' : 'd626cfb8a9712cb92b820798ab5bc1f8',
                        'openmp' : '121ddb10167d7fc38b1f7e4b029cf059',
                        'libcxx' : '406f09b1dab529f3f7879f4d548329d2',
                        'libcxxabi' : 'b22c707e8d474a99865ad3c521c3d464',
                        'clang' : '93f9532f8f7e6f1d8e5c1116907051cb',
                        'clang-tools-extra' : 'f13f31ed3038acadc6fa63fef812a246',
                        'lldb' : 'cc5ea8a414c62c33e760517f8929a204',
                        }
                  },
               ]

    for release in releases:
        version(release['version'], release['md5'], url=llvm_url % release)

        for name, md5 in release['resources'].items():
            resource(name=name,
                     url=resources[name]['url'] % release,
                     md5=md5,
                     destination=resources[name]['destination'],
                     when='@%(version)s' % release,
                     placement=resources[name].get('placement', None))

    def install(self, spec, prefix):
        env['CXXFLAGS'] = self.compiler.cxx11_flag
        cmake_args = [ arg for arg in std_cmake_args if 'BUILD_TYPE' not in arg ]

        build_type = 'RelWithDebInfo'  if '+debug' in spec else 'Release'
        cmake_args.extend([
                '..',
                '-DCMAKE_BUILD_TYPE=' + build_type,
                '-DLLVM_REQUIRES_RTTI:BOOL=ON',
                '-DCLANG_DEFAULT_OPENMP_RUNTIME:STRING=libomp',
                '-DPYTHON_EXECUTABLE:PATH=%s/bin/python' % spec['python'].prefix ])

        if '+lto' in spec:
            cmake_args.append('-DLLVM_BINUTILS_INCDIR=' + os.path.join( spec['binutils'].prefix, 'include'))
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

        if  '+clang' not in spec:
            if '+clang_extra' in spec:
                raise SpackException('The clang_extra variant requires the clang variant to be selected')
            if '+lldb' in spec:
                raise SpackException('The lldb variant requires the clang variant to be selected')

        with working_dir('spack-build', create=True):
            make("install")
            query_path = os.path.join('bin', 'clang-query')
            # Manually install clang-query, because llvm doesn't...
            if os.path.exists(query_path):
                shutil.copy(query_path, os.path.join(prefix, 'bin'))
