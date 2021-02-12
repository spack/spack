# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyOrTools(CMakePackage):
    """This project hosts operations research tools developed at
    Google and made available as open source under the Apache 2.0
    License."""

    homepage = "https://developers.google.com/optimization/"
    url      = "https://github.com/google/or-tools/archive/v7.8.tar.gz"

    version('8.1.8487', sha256='3b637939202ff209a234a3953e1794ed6b2aed09036d302434e51b868a7aac63')
    version('8.1',      sha256='5359291f2ddb7f9a1321dc9bdc5d714592697cc87d6d44d448c3684ff899a99b')
    version('8.0.8283', sha256='b810b52ab220e95b79491b92fcf3c7cd70d371779076a07e7141e6f69b05f0b0')
    version('8.0',      sha256='4151b549492e1270a1c469a0f486282035661db7fb7e27f338d5e32457a8dc23')
    version('7.8.7959', sha256='881e95dd23ecb8af635fb31ba78d715c7b03631354f715bc4f7dd241523a24c3')
    version('7.8', sha256='d93a9502b18af51902abd130ff5f23768fcf47e266e6d1f34b3586387aa2de68')

    depends_on('cmake@3.14:', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-protobuf@3.12.2:', type=('build', 'run'))
    depends_on('protobuf@3.12.2:')
    depends_on('py-six@1.10:', type=('build', 'run'))
    depends_on('gflags@2.2.2')
    depends_on('glog@0.4.0')
    depends_on('protobuf@3.12.2')
    depends_on('abseil-cpp@20200225.2')
    depends_on('cbc@2.10.5')
    depends_on('cgl@0.60.3')
    depends_on('clp@1.17.4')
    depends_on('osi@0.108.6')
    depends_on('coinutils@2.11.4')
    depends_on('swig')
    depends_on('python', type=('build', 'run'))
    depends_on('py-wheel', type='build')
    depends_on('py-virtualenv', type='build')
    depends_on('scipoptsuite')

    extends('python')

    def cmake_args(self):
        cmake_args = []
        cmake_args.append('-DBUILD_DEPS=OFF')
        cmake_args.append('-DBUILD_PYTHON=ON')
        cmake_args.append('-DBUILD_TESTING=OFF')
        return cmake_args

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make("install")
        with working_dir(join_path(self.build_directory, 'python')):
            setup_py('install', '--prefix=' + prefix,
                     '--single-version-externally-managed', '--root=/')
