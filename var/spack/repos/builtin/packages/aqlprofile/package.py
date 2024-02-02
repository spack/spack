# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Aqlprofile(Package):
    """
    HSA extension AMD AQL profile library.
    Provides AQL packets helper methods for perfcounters (PMC) and SQ threadtraces (SQTT).
    """

    maintainers("afzpatel", "srekolam", "renjithravindrankannath")

    version(
        ver="6.0.0",
        sha256="578bf9b21fa55af702413011ebf75ee53e0233399ea0732b23a68b2881bffe55",
        url="http://localhost:8000/6.0.0/aqlprofile-6.0.0.tar.gz",
    )
    version(
        ver="5.7.1",
        sha256="597b61ef24f1c6001735e145f3682ebd83999cd0486f63fffff8cfaad46405f0",
        url="http://localhost:8000/5.7.1/aqlprofile-5.7.1.tar.gz",
    )
    version(
        ver="5.7.0",
        sha256="43fd6468714d4c38860d26c6e169587896d34a02ce0204b8cb1b6baf44fc1bc3",
        url="http://localhost:8000/5.7.0/aqlprofile-5.7.0.tar.gz",
    )
    version(
        ver="5.6.1",
        sha256="23dd3e7d7fc7b5eb67f1e8fb6b3b527f1cffd513cd5ab2acc513d8a4ff1bcae8",
        url="http://localhost:8000/5.6.1/aqlprofile-5.6.1.tar.gz",
    )
    version(
        ver="5.6.0",
        sha256="d086ba5a1460602a5fa2ca3196049bd6938f883247ff8b70e06c52a5e330c3c3",
        url="http://localhost:8000/5.6.0/aqlprofile-5.6.0.tar.gz",
    )
    version(
        ver="5.5.1",
        sha256="8e85781ba320c1ffe5904b2a6e79388fc564e08cc3893dc69b2f70d142b6a724",
        url="http://localhost:8000/5.5.1/aqlprofile-5.5.1.tar.gz",
    )
    version(
        ver="5.5.0",
        sha256="547b51c9e41e081cbaf3078bfddfe296e86d06ebfdf51a82d61824e8caf1e876",
        url="http://localhost:8000/5.5.0/aqlprofile-5.5.0.tar.gz",
    )

    def install(self, spec, prefix):
        install_tree("share", prefix.share)
        install_tree("lib", prefix.lib)
