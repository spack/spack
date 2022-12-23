# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path
import posixpath

import spack.tengine

from .base import Reporter


class JUnit(Reporter):
    """Generate reports of spec installations for JUnit."""

    def concretization_report(self, filename, msg):
        pass

    def __init__(self):
        # Jinja2 expects `/` path separators
        self.template_file = "reports/junit.xml"

    def build_report(self, filename, report_data):
        if not (os.path.splitext(filename))[1]:
            # Ensure the report name will end with the proper extension;
            # otherwise, it currently defaults to the "directory" name.
            filename = filename + ".xml"

        # Write the report
        with open(filename, "w") as f:
            env = spack.tengine.make_environment()
            t = env.get_template(self.template_file)
            f.write(t.render(report_data))

    def test_report(self, filename, report_data):
        self.build_report(filename, report_data)
