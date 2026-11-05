# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class Dependentcallback(Package):
    homepage = "http://www.example.com"
    url = "http://www.example.com/dependent-callback-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    @run_before_dependent("callbacks", when="@1.0")
    def matching_conditional_callback(self, dependent_pkg):
        os.environ["MATCHING_DEPENDENT_CALLBACK"] = dependent_pkg.name

    @run_before_dependent("callbacks", when="@2.0")
    def nonmatching_conditional_callback(self, dependent_pkg):
        os.environ["NONMATCHING_DEPENDENT_CALLBACK"] = dependent_pkg.name

    @run_before_dependent("callbacks@3:")
    def nonmatching_dependent_callback(self, dependent_pkg):
        os.environ["NONMATCHING_DEPENDENT_SPEC_CALLBACK"] = dependent_pkg.name

    @run_before_dependent("callbacks")
    def before_dependent_install(self, dependent_pkg):
        os.environ["BEFORE_DEPENDENT_INSTALL_CALLED"] = dependent_pkg.name
        os.environ["BEFORE_DEPENDENT_INSTALL_VALUE"] = os.environ.get("TEST_VALUE", "unset")

    @run_after_dependent("callbacks")
    def after_dependent_last_phase(self, dependent_pkg):
        os.environ["AFTER_DEPENDENT_LAST_PHASE_CALLED"] = dependent_pkg.name
        os.environ["AFTER_DEPENDENT_LAST_PHASE_VALUE"] = os.environ["TEST_VALUE"]
