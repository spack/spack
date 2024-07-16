# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Mpich(Package):

    homepage = "https://www.example.com"
    has_code = False


    provides("mpi")

    version("1.0")    
    provides("mpi@1", when="@1.0")
    can_splice("xmpi@6.0 abi=mpich", when="@1.0")

    version("2.0")    
    provides("mpi@2", when="@2.0")
    can_splice("xmpi@7.0 abi=mpich", when="@2.0")

    version("3.0")    
    provides("mpi@3", when="@3.0")
    can_splice("xmpi@8.0 abi=mpich", when="@3.0")


    def install(self, spec, prefix):
        touch(prefix.foo)