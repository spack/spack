# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Reporter:
    """Base class for report writers."""

    def build_report(self, filename: str, report_data: str):
        raise NotImplementedError("must be implemented by derived classes")

    def test_report(self, filename: str, report_data: str):
        raise NotImplementedError("must be implemented by derived classes")

    def concretization_report(self, filename: str, msg: str):
        raise NotImplementedError("must be implemented by derived classes")
