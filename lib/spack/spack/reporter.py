# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


__all__ = ['Reporter']


class Reporter(object):
    """Base class for report writers."""

    def __init__(self, install_command, cdash_upload_url):
        self.install_command = install_command
        self.cdash_upload_url = cdash_upload_url

    def build_report(self, filename, report_data):
        pass

    def concretization_report(self, filename, msg):
        pass
