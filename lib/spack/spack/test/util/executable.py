# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import llnl.util.filesystem as fs

import spack.util.executable as ex
from spack.hooks.sbang import filter_shebangs_in_directory


def test_read_unicode(tmpdir):
    script_name = 'print_unicode.py'

    with tmpdir.as_cwd():

        # make a script that prints some unicode
        with open(script_name, 'w') as f:
            f.write('''#!{0}
from __future__ import print_function
import sys
if sys.version_info < (3, 0, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
print(u'\\xc3')
'''.format(sys.executable))

        # make it executable
        fs.set_executable(script_name)
        filter_shebangs_in_directory('.', [script_name])

        # read the unicode back in and see whether things work
        script = ex.Executable('./%s' % script_name)
        assert u'\xc3' == script(output=str).strip()
