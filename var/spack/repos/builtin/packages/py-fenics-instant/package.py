# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFenicsInstant(PythonPackage):
    """**This package is retired and not any more in use by FEniCS.**
    Instant is a Python module that allows for instant inlining of C and
    C++ code in Python. It is a small Python module built on top of SWIG
    and Distutils."""

    homepage = "https://fenicsproject.org/"
    git      = "https://bitbucket.org/fenics-project/instant.git"
    url      = "https://bitbucket.org/fenics-project/instant/get/2017.2.0.tar.gz"

    version('2017.2.0',       sha256='517f4ff355704420c5938e6fe33e97892856e136732de86ffa29bb996b445791')
    version('2017.1.0.post1', sha256='f83797187753a6a3fcede19e9ccb2cbef8635ac7af465ba56ef384e39961f577')
    version('2017.1.0',       sha256='24c4571240e8a24a54d830d92b3a3239f8e77f491943837ae24f583fd791f781')
    version('2016.2.0',       sha256='2fb4f6cf087369ca11482a945ae695066f4b9aca15d90e033f059ea1107bb874')
    version('2016.1.0',       sha256='0ec1ac2db9dddae1d299ab86e2dedd7730238bbbe683095c177e19fe5c7e7108')
    version('1.6.0',          sha256='a9c569b3fa5ce5f00465323cf53da116f4cf3d416920b5628acbdcdc15b892a7')
    version('1.5.0',          sha256='16b449dea0f69e6dd0edb968b8bc34137475223cbb8556dfea2637edef25f5ab')
    version('1.4.0',          sha256='05016cf26740259c408d19b125f2326206c59d2a7d30614e94903d50bf73c843')
    version('1.3.0',          sha256='348226ef1a43793442a88a095c0078c204ce1f86bd8749e01d16def8c57abb76')

    def url_for_version(self, version):
        url = "https://bitbucket.org/fenics-project/instant/get"
        if version >= Version('2017.1.0'):
            url += "/{0}.tar.gz".format(version)
        else:
            url += "/instant-{0}.tar.gz".format(version)
        return url
