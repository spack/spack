# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import Any, Dict, List


class Reporter:
    """Base class for report writers.

    The output location is a file or a directory depending on the reporter, so parameters are
    positional-only (``__`` prefix) and subclasses may name them as they see fit.
    """

    def build_report(self, __filename: str, __specs: List[Dict[str, Any]]):
        raise NotImplementedError("must be implemented by derived classes")

    def test_report(self, __filename: str, __specs: List[Dict[str, Any]]):
        raise NotImplementedError("must be implemented by derived classes")

    def concretization_report(self, __filename: str, __msg: str):
        raise NotImplementedError("must be implemented by derived classes")
