# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libffi(AutotoolsPackage):
    """The libffi library provides a portable, high level programming
    interface to various calling conventions. This allows a programmer
    to call any function specified by a call interface description at
    run time."""
    homepage = "https://sourceware.org/libffi/"

    version('3.2.1', '83b89587607e3eb65c70d361f13bab43',
            url="https://www.mirrorservice.org/sites/sourceware.org/pub/libffi/libffi-3.2.1.tar.gz")
    variant("shared", default=True, description="Enable shared libs")

    def configure_args(self):
        args = []
        if "+shared" in self.spec:
            args.append("--enable-shared")
        else:
            args.append("--disable-shared")
        
        if self.spec.satisfies("%intel") and self.spec.satisfies("os=cnl5"):
            args.append("--host=x86_64")

        return args
    # version('3.1', 'f5898b29bbfd70502831a212d9249d10',url =
    # "ftp://sourceware.org/pub/libffi/libffi-3.1.tar.gz") # Has a bug
    # $(lib64) instead of ${lib64} in libffi.pc

    @property
    def headers(self):
        # The headers are probably in self.prefix.lib but we search everywhere
        return find_headers('ffi', self.prefix, recursive=True)
