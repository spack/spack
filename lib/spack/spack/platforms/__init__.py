# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from ._functions import by_name, host, platforms
from ._platform import Platform
from .cray import Cray
from .darwin import Darwin
from .linux import Linux
from .test import Test

__all__ = [
    'Platform',
    'Cray',
    'Darwin',
    'Linux',
    'Test',
    'platforms',
    'host',
    'by_name'
]
