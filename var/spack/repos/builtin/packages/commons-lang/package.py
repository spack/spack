# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CommonsLang(Package):
    """The standard Java libraries fail to provide enough methods for
    manipulation of its core classes. Apache Commons Lang provides these
    extra methods.

    Lang provides a host of helper utilities for the java.lang API, notably
    String manipulation methods, basic numerical methods, object reflection,
    concurrency, creation and serialization and System properties. Additionally
    it contains basic enhancements to java.util.Date and a series of utilities
    dedicated to help with building methods, such as hashCode, toString and
    equals."""

    homepage = "http://commons.apache.org/proper/commons-lang/"
    url      = "https://archive.apache.org/dist/commons/lang/binaries/commons-lang-2.6-bin.tar.gz"

    version('2.6', '444075803459bffebfb5e28877861d23')
    version('2.4', '5ff5d890e46021a2dbd77caba80f90f2')

    extends('jdk')
    depends_on('java@2:', type='run')

    def install(self, spec, prefix):
        install('commons-lang-{0}.jar'.format(self.version), prefix)
