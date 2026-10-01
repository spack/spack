# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack_repo.builtin_mock.build_systems.generic import GenericBuilder, Package

from spack.package import *


class Builderdependentcallback(Package):
    homepage = "http://www.example.com"
    url = "http://www.example.com/builder-dependent-callback-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")


class GenericBuilder(GenericBuilder):
    @run_after_dependent("install")
    def builder_dependent_callback(self, dependent_pkg):
        os.environ["BUILDER_DEPENDENT_CALLBACK"] = dependent_pkg.name
