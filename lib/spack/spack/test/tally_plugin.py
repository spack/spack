##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os

from nose.plugins import Plugin


class Tally(Plugin):
    name = 'tally'

    def __init__(self):
        super(Tally, self).__init__()
        self.successCount = 0
        self.failCount = 0
        self.errorCount = 0
        self.error_list = []
        self.fail_list = []

    @property
    def numberOfTestsRun(self):
        """Excludes skipped tests"""
        return self.errorCount + self.failCount + self.successCount

    def options(self, parser, env=os.environ):
        super(Tally, self).options(parser, env=env)

    def configure(self, options, conf):
        super(Tally, self).configure(options, conf)

    def addSuccess(self, test):
        self.successCount += 1

    def addError(self, test, err):
        self.errorCount += 1
        self.error_list.append(test)

    def addFailure(self, test, err):
        self.failCount += 1
        self.fail_list.append(test)

    def finalize(self, result):
        pass
