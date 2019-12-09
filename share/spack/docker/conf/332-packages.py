# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

class SpackBootstrap(BundlePackage):
    version('1.0')
    depends_on('autoconf')
    depends_on('automake')
    depends_on('binutils')
    depends_on('bzip2')
    depends_on('cmake @3.15.5 -ncurses -qt')
    depends_on('coreutils')
    depends_on('curl')
    depends_on('diffutils')
    depends_on('environment-modules')
    depends_on('file')
    depends_on('git')
    depends_on('gmake')
    depends_on('gnupg')
    depends_on('grep')
    depends_on('gzip')
    depends_on('m4')
    depends_on('nano')
    depends_on('patch')
    depends_on('patchelf')
    depends_on('procps')
    depends_on('py-boto3')
    depends_on('py-pip')
    depends_on('python @3.7.4'
            ' +bz2'
            ' +ctypes'
            ' +dbm'
            ' +lzma'
            ' +optimizations'
            ' +pic'
            ' +pyexpat'
            ' +pythoncmd'
            ' +readline'
            ' +sqlite3'
            ' +ssl'
            ' +uuid'
            ' +zlib')
    depends_on('sed')
    depends_on('tar')
    depends_on('tcl')
    depends_on('unzip')
    depends_on('xz')
    depends_on('zlib')
