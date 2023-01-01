# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ExecutableWrapper(MakefilePackage):
    """An interpreter for a scripting language to manage environment
    variables before running an executable."""

    homepage = "https://github.com/haampie/executable-wrapper"
    url = "https://github.com/haampie/executable-wrapper/releases/download/v0.1.0/executable-wrapper-0.1.0.tar.gz"

    maintainers = ["haampie"]

    version("0.1.0", sha256="3d5a84404f3a082d733dfba79b6aeec90cd0b425b111a38424b0143e2730c507")

    def install(self, spec, prefix):
        make("install", "prefix={}".format(prefix))

