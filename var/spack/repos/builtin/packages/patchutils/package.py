# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Patchutils(AutotoolsPackage):
    """This is patchutils, a collection of tools that operate on patch
    files."""

    homepage = "https://github.com/twaugh/patchutils"
    url      = "https://github.com/twaugh/patchutils/archive/0.4.2.tar.gz"

    version('0.4.2', sha256='2ff95f11946558ce63f4d1167abaccbffd49750152346d5304e03ad884304ad6')
    version('0.4.0', sha256='7c693849a1a18688fbe1bddac38847fb56e467a749aabc7c671c9fe353049323')
    version('0.3.4', sha256='49510da6a9627bfe3c340eed69040ca513cdc56d0bc82dacec07c13e766ba550')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
