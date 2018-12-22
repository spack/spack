# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CommonsLang3(Package):
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
    url      = "https://archive.apache.org/dist/commons/lang/binaries/commons-lang3-3.7-bin.tar.gz"

    version('3.7', 'c7577443639dc6efadc80f1cbc7fced5')

    extends('jdk')
    depends_on('java@7:', type='run')

    def install(self, spec, prefix):
        install('commons-lang3-{0}.jar'.format(self.version), prefix)
