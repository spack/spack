# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

class CmakeConditionalVariantsTest(CMakePackage):
    homepage = "https://dev.null"
    version('1.0')
    variant('example', default=True, description='nope', when='@2.0:')
