# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libseccomp(AutotoolsPackage):
    """The main libseccomp repository"""

    homepage = "https://github.com/seccomp/libseccomp"
    url      = "https://github.com/seccomp/libseccomp/archive/v2.3.3.zip"

    version('2.5.1', sha256='6b9e2f4b37c213ee3d33daad3ee136ac2a58c91b8d7e6ba74c4f73ad6f9764ce')
    version('2.5.0', sha256='c463aab67cad86950b61d2db6528adb9454305d5c228d74460166a35b0e90b59')
    version('2.4.4', sha256='d53d2b1bbd772260a68a9bce736bda8fc8a110b78d910db1fdc61f4e13fd7423')
    version('2.4.3', sha256='5d3de27bc501b15a8ddbee208a1d945390d5a07a001588e5142e0c283d323c97')
    version('2.4.2', sha256='f16308c583f2c808e97361cef5fb2c8e853bc78d5ede4cc186faac83c1d2c5ec')
    version('2.4.1', sha256='00e471ac08d828e1e68c2b6bf92e3a8ac3b07c0a407df191aeae9eacc0144258')
    version('2.4.0', sha256='5f35a8abbfd7677592a378a45396066181bf71e71c241136f7599b2974d41670')
    version('2.3.3', sha256='627e114b3be2e66ed8d88b90037498333384d9bea822423662a44c3a8520e187')

    variant('python', default=True, description="Build Python bindings")

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on("py-cython", type="build", when="+python")

    def configure_args(self):
        args = []
        if "+python" in self.spec:
            args.append("--enable-python")
        return args
