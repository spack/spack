# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys

from spack_repo.builtin_mock.build_systems.generic import Package
from spack.cmd.mirror import evaluate_or_true_if_mirror_all
from spack.package import *
import platform

class ArchSpecificPkg(Package):
    if evaluate_or_true_if_mirror_all(platform.machine() == "x86_64"):
        print("Adding x86_64 version")
        version("1.0", sha256="a" * 64)
    if evaluate_or_true_if_mirror_all(platform.machine() == "aarch64"):
        print("Adding aarch64 version")
        version("1.0", sha256="b" * 64)
