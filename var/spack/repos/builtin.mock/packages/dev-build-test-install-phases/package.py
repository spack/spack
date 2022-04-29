# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class DevBuildTestInstallPhases(Package):
    homepage = "example.com"
    url = "fake.com"

    version('0.0.0', sha256='0123456789abcdef0123456789abcdef')

    def install(self, spec, prefix):
        print("install")
