##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from nose.plugins import Plugin

import os

class Tally(Plugin):
    name = 'tally'

    def __init__(self):
        super(Tally, self).__init__()
        self.successes = set()
        self.failures = set()
        self.errors = set()

    @property
    def successCount(self):
        return len(self.successes)
    
    @property
    def failCount(self):
        return len(self.failures)
    
    @property
    def errorCount(self):
        return len(self.errors)
    
    @property
    def numberOfTests(self):
        return self.errorCount + self.failCount + self.successCount

    def options(self, parser, env=os.environ):
        super(Tally, self).options(parser, env=env)

    def configure(self, options, conf):
        super(Tally, self).configure(options, conf)

    def begin(self):
        print ">>> TALLY PLUGIN BEGIN"

    def addSuccess(self, test):
        self.successes.add(test)
        
    def addError(self, test, err):
        self.errors.add(test)
            
    def addFailure(self, test, err):
        test.failures.add(test)

    def finalize(self, result):
        pass
