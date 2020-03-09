# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Activeharmony(Package):
    """Active Harmony: a framework for auto-tuning (the automated search for
       values to improve the performance of a target application)."""
    homepage = "http://www.dyninst.org/harmony"
    url      = "http://www.dyninst.org/sites/default/files/downloads/harmony/ah-4.5.tar.gz"

    version('4.5', sha256='31d9990c8dd36724d336707d260aa4d976e11eaa899c4c7cc11f80a56cdac684')

    def install(self, spec, prefix):
        make("CFLAGS=-O3")
        make("install", 'PREFIX=%s' % prefix)
