# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Filebench(AutotoolsPackage):
    """
    Filebench is a file system and storage benchmark that can generate a
    large variety of workloads. Unlike typical benchmarks it is extremely
    flexible and allows to specify application's I/O behavior using its
    extensive Workload Model Language (WML). Users can either describe
    desired workloads from scratch or use(with or without modifications)
    workload personalities shipped with Filebench(e.g., mail-, web-, file-,
    and database-server workloads). Filebench is equally good for micro
    and macro-benchmarking, quick to setup, and relatively easy to use.
    """

    homepage = "https://github.com/filebench/filebench"
    url      = "https://github.com/filebench/filebench/archive/1.5-alpha3.tar.gz"

    version('1.5-alpha3', sha256='2dedfc46458f5bb13e5f5a4a9f4db6263152f6186690d57653c96138610db35a')
    version('1.5-alpha2', sha256='02aeae7bd7e6c3e1d32862a4d1c5e14e59a1ffbb8fadbf09dc84ebe82bc6029e')
    version('1.5-alpha1', sha256='8266c25274a20025c325050ed4050d2783d239f77558fc332381d05de9917dfc')
    version('1.4.9.1',    sha256='77ae91b83c828ded1219550aec74fbbd6975dce02cb5ab13c3b99ac2154e5c2e', preferred=True)
    version('1.4.9',      sha256='61b8a838c1450b51a4ce61481a19a1bf0d6e3993180c524ff4051f7c18bd9c6a')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('flex',     type='build')
    depends_on('bison',    type='build')

    def autoreconf(self, spec, prefix):
        sh = which('sh')
        sh('libtoolize')
        sh('aclocal')
        sh('autoheader')
        sh('autoheader')
        sh_automake = Executable('automake --add-missing')
        sh_automake()
        sh('autoconf')
