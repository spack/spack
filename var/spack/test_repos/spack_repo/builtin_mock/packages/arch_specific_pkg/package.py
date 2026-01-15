# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import platform

from spack_repo.builtin_mock.build_systems.generic import Package

import spack.mirrors.utils
from spack.package import *


class ArchSpecificPkg(Package):
    version("1.0", sha256="a" * 64, url="https://example.com/pkg-1.0-a.tar.gz")
    if spack.mirrors.utils.evaluate_or_true_if_mirror_all(False):
        version("1.0", sha256="b" * 64, url="https://example.com/pkg-1.0-b.tar.gz")
