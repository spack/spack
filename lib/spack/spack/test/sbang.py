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
"""\
Test that Spack's shebang filtering works correctly.
"""
import os
import unittest
import tempfile
import shutil

from llnl.util.filesystem import *
from spack.hooks.sbang import filter_shebangs_in_directory
import spack

short_line = "#!/this/is/short/bin/bash\n"
long_line  = "#!/this/" + ('x' * 200) + "/is/long\n"
sbang_line = '#!/bin/bash %s/bin/sbang\n' % spack.spack_root
last_line = "last!\n"

class SbangTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

        # make sure we can ignore non-files
        directory = os.path.join(self.tempdir, 'dir')
        mkdirp(directory)

        # Script with short shebang
        self.short_shebang = os.path.join(self.tempdir, 'short')
        with open(self.short_shebang, 'w') as f:
            f.write(short_line)
            f.write(last_line)

        # Script with long shebang
        self.long_shebang = os.path.join(self.tempdir, 'long')
        with open(self.long_shebang, 'w') as f:
            f.write(long_line)
            f.write(last_line)

        # Script already using sbang.
        self.has_shebang = os.path.join(self.tempdir, 'shebang')
        with open(self.has_shebang, 'w') as f:
            f.write(sbang_line)
            f.write(long_line)
            f.write(last_line)


    def tearDown(self):
         shutil.rmtree(self.tempdir, ignore_errors=True)



    def test_shebang_handling(self):
        filter_shebangs_in_directory(self.tempdir)

        # Make sure this is untouched
        with open(self.short_shebang, 'r') as f:
            self.assertEqual(f.readline(), short_line)
            self.assertEqual(f.readline(), last_line)

        # Make sure this got patched.
        with open(self.long_shebang, 'r') as f:
            self.assertEqual(f.readline(), sbang_line)
            self.assertEqual(f.readline(), long_line)
            self.assertEqual(f.readline(), last_line)

        # Make sure this is untouched
        with open(self.has_shebang, 'r') as f:
            self.assertEqual(f.readline(), sbang_line)
            self.assertEqual(f.readline(), long_line)
            self.assertEqual(f.readline(), last_line)
