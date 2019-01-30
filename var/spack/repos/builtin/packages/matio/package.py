# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Matio(AutotoolsPackage):
    """matio is an C library for reading and writing Matlab MAT files"""
    homepage = "http://sourceforge.net/projects/matio/"
    url = "http://downloads.sourceforge.net/project/matio/matio/1.5.9/matio-1.5.9.tar.gz"

    version('1.5.9', 'aab5b4219a3c0262afe7eeb7bdd2f463')
    version('1.5.2', '85b007b99916c63791f28398f6a4c6f1')

    variant("zlib", default=True,
            description='support for compressed mat files')
    variant("hdf5", default=True,
            description='support for version 7.3 mat files via hdf5')
    variant("shared", default=True, description='Enables the build of shared libraries.')

    depends_on("zlib", when="+zlib")
    depends_on("hdf5", when="+hdf5")

    def configure_args(self):
        args = []
        if '+zlib' in self.spec:
            args.append("--with-zlib=%s" % self.spec['zlib'].prefix)
        if '+hdf5' in self.spec:
            args.append("--with-hdf5=%s" % self.spec['hdf5'].prefix)
        if '+shared' not in self.spec:
            args.append("--disable-shared")
        return args
