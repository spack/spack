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
"""
This test ensures that all Spack files are Python version 2.6 or less.

Spack was originally 2.7, but enough systems in 2014 are still using
2.6 on their frontend nodes that we need 2.6 to get adopted.
"""
import os
import re
import unittest

import llnl.util.tty as tty
import pyqver2
import spack

spack_max_version = (2,6)

class PythonVersionTest(unittest.TestCase):

    def pyfiles(self, *search_paths):
        # first file is the spack script.
        yield spack.spack_file

        # Iterate through the whole spack source tree.
        for path in search_paths:
            for root, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    if re.match(r'^[^.#].*\.py$', filename):
                        yield os.path.join(root, filename)


    def package_py_files(self):
        for name in spack.repo.all_package_names():
            yield spack.repo.filename_for_package_name(name)


    def check_python_versions(self, *files):
        # dict version -> filename -> reasons
        all_issues = {}

        for fn in files:
            with open(fn) as pyfile:
                versions = pyqver2.get_versions(pyfile.read())
                for ver, reasons in versions.items():
                    if ver > spack_max_version:
                        if not ver in all_issues:
                            all_issues[ver] = {}
                        all_issues[ver][fn] = reasons

        if all_issues:
            tty.error("Spack must run on Python version %d.%d"
                      % spack_max_version)

        for v in sorted(all_issues.keys(), reverse=True):
            msgs = []
            for fn in sorted(all_issues[v].keys()):
                short_fn = fn
                if fn.startswith(spack.prefix):
                    short_fn = fn[len(spack.prefix):]

                reasons = [r for r in set(all_issues[v][fn]) if r]
                for r in reasons:
                    msgs.append(("%s:%s" % ('spack' + short_fn, r[0]), r[1]))

            tty.error("These files require version %d.%d:" % v)
            maxlen = max(len(f) for f, prob in msgs)
            fmt = "%%-%ds%%s" % (maxlen+3)
            print fmt % ('File', 'Reason')
            print fmt % ('-' * (maxlen), '-' * 20)
            for msg in msgs:
                print fmt % msg

        self.assertTrue(len(all_issues) == 0)


    def test_core_module_compatibility(self):
        self.check_python_versions(*self.pyfiles(spack.lib_path))


    def test_package_module_compatibility(self):
        self.check_python_versions(*self.pyfiles(spack.packages_path))
