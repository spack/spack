# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Opari2(AutotoolsPackage):
    """OPARI2 is a source-to-source instrumentation tool for OpenMP and hybrid
    codes. It surrounds OpenMP directives and runtime library calls with calls
    to the POMP2 measurement interface. OPARI2 will provide you with a new
    initialization method that allows for multi-directory and parallel builds
    as well as the usage of pre-instrumented libraries. Furthermore, an
    efficient way of tracking parent-child relationships was added.
    Additionally, we extended OPARI2 to support instrumentation of OpenMP 3.0
    tied tasks.
    """

    homepage = "http://www.vi-hps.org/projects/score-p"
    url      = "https://www.vi-hps.org/cms/upload/packages/opari2/opari2-2.0.4.tar.gz"

    version('2.0.5', '9034dd7596ac2176401090fd5ced45d0ab9a9404444ff767f093ccce68114ef5')
    version('2.0.4', 'f69e324792f66780b473daf2b3c81f58ee8188adc72b6fe0dacf43d4c1a0a131')
    version('2.0.3', 'f34674718ffdb098a48732a1eb9c1aa2')
    version('2.0.1', '74af78f1f27b8caaa4271e0b97fb0fba')
    version('2.0',   '72350dbdb6139f2e68a5055a4f0ba16c')
    version('1.1.4', '245d3d11147a06de77909b0805f530c0')
    version('1.1.2', '9a262c7ca05ff0ab5f7775ae96f3539e')

    def configure_args(self):
        return ["--enable-shared"]
