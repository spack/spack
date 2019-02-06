# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Gdbm(AutotoolsPackage):
    """GNU dbm (or GDBM, for short) is a library of database functions
    that use extensible hashing and work similar to the standard UNIX dbm.
    These routines are provided to a programmer needing to create and
    manipulate a hashed database."""

    homepage = "http://www.gnu.org.ua/software/gdbm/gdbm.html"
    url      = "https://ftpmirror.gnu.org/gdbm/gdbm-1.13.tar.gz"

    version('1.18.1', '86e613527e5dba544e73208f42b78b7c022d4fa5a6d5498bf18c8d6f745b91dc')
    version('1.14.1', 'c2ddcb3897efa0f57484af2bd4f4f848')
    version('1.13',  '8929dcda2a8de3fd2367bdbf66769376')
    version('1.12',  '9ce96ff4c99e74295ea19040931c8fb9')
    version('1.11',  '72c832680cf0999caedbe5b265c8c1bd')
    version('1.10',  '88770493c2559dc80b561293e39d3570')
    version('1.9.1', '59f6e4c4193cb875964ffbe8aa384b58')
    version('1.9',   '1f0e8e6691edd61bdd6b697b8c02528d')

    depends_on("readline")

    def configure_args(self):

        # GDBM uses some non-standard GNU extensions,
        # enabled with -D_GNU_SOURCE.  See:
        #   https://patchwork.ozlabs.org/patch/771300/
        #   https://stackoverflow.com/questions/5582211
        #   https://www.gnu.org/software/automake/manual/html_node/Flag-Variables-Ordering.html
        return [
            '--enable-libgdbm-compat',
            'CPPFLAGS=-D_GNU_SOURCE']
