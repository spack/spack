# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import platform

from spack_repo.builtin_mock.build_systems.generic import Package

import spack.mirrors.utils
from spack.package import *


class ArchSpecificPkg(Package):
    if spack.mirrors.utils.evaluate_or_true_if_mirror_all(platform.machine() == "x86_64"):
        print("Adding x86_64 version")
        version("1.0", sha256="a" * 64, url="https://example.com/pkg-1.0-x86_64.tar.gz")
    if spack.mirrors.utils.evaluate_or_true_if_mirror_all(platform.machine() == "aarch64"):
        print("Adding aarch64 version")
        version("1.0", sha256="b" * 64, url="https://example.com/pkg-1.0-aarch64.tar.gz")
