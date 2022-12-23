# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Reporter:
    """Base class for report writers."""

    def __init__(self, args):
        self.args = args

    def build_report(self, filename, report_data):
        raise NotImplementedError("must be implemented by derived classes")

    def test_report(self, filename, report_data):
        raise NotImplementedError("must be implemented by derived classes")

    def concretization_report(self, filename, msg):
        raise NotImplementedError("must be implemented by derived classes")


class NullReporter(Reporter):
    """A reporter that does nothing"""

    def concretization_report(self, filename, msg):
        pass

    def test_report(self, filename, report_data):
        pass

    def build_report(self, filename, report_data):
        pass
