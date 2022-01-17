# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from time import sleep


class DevBuildTestInstallPhases(Package):
    homepage = "example.com"
    url = "fake.com"

    version('0.0.0', sha256='0123456789abcdef0123456789abcdef')

    phases = ['one', 'two', 'three', 'install']

    def one(self, spec, prefix):
        sleep(1)
        print("One locomoco")

    def two(self, spec, prefix):
        sleep(2)
        print("Two locomoco")

    def three(self, spec, prefix):
        sleep(3)
        print("Three locomoco")

    def install(self, spec, prefix):
        print("install")
