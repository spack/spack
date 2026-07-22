# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from .common import (
    executable_prefix,
    set_virtuals_nonbuildable,
    spec_from_detection,
    update_configuration,
)
from .path import by_path, executables_in_path
from .test import detection_tests

__all__ = [
    "by_path",
    "executables_in_path",
    "executable_prefix",
    "spec_from_detection",
    "update_configuration",
    "set_virtuals_nonbuildable",
    "detection_tests",
]
