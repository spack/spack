# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Callpath(CMakePackage):
    """Library for representing callpaths consistently in
       distributed-memory performance tools."""

    homepage = "https://github.com/llnl/callpath"
    url      = "https://github.com/llnl/callpath/archive/v1.0.1.tar.gz"

    version('1.0.4', '39d2e06bfa316dec1085b874092e4b08')
    version('1.0.2', 'b1994d5ee7c7db9d27586fc2dcf8f373')
    version('1.0.1', '0047983d2a52c5c335f8ba7f5bab2325')

    depends_on('elf', type='link')
    depends_on('libdwarf')
    depends_on('dyninst')
    depends_on('adept-utils')
    depends_on('mpi')
    depends_on('cmake@2.8:', type='build')

    def cmake_args(self):
        # TODO: offer options for the walker used.
        args = ["-DCALLPATH_WALKER=dyninst"]

        if self.spec.satisfies("^dyninst@9.3.0:"):
            std_flag = self.compiler.cxx11_flag
            args.append("-DCMAKE_CXX_FLAGS='{0} -fpermissive'".format(
                std_flag))

        return args
