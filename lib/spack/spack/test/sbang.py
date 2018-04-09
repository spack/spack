##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import stat
import pytest
import tempfile
import shutil
import filecmp

from llnl.util.filesystem import mkdirp

import spack.paths
from spack.hooks.sbang import shebang_too_long, filter_shebangs_in_directory
from spack.util.executable import which


short_line        = "#!/this/is/short/bin/bash\n"
long_line         = "#!/this/" + ('x' * 200) + "/is/long\n"
lua_line          = "#!/this/" + ('x' * 200) + "/is/lua\n"
lua_in_text       = ("line\n") * 100 + "lua\n" + ("line\n" * 100)
lua_line_patched  = "--!/this/" + ('x' * 200) + "/is/lua\n"
node_line         = "#!/this/" + ('x' * 200) + "/is/node\n"
node_in_text      = ("line\n") * 100 + "lua\n" + ("line\n" * 100)
node_line_patched = "//!/this/" + ('x' * 200) + "/is/node\n"
sbang_line        = '#!/bin/bash %s/bin/sbang\n' % spack.paths.prefix
last_line         = "last!\n"


class ScriptDirectory(object):
    """Directory full of test scripts to run sbang instrumentation on."""
    def __init__(self):
        self.tempdir = tempfile.mkdtemp()

        self.directory = os.path.join(self.tempdir, 'dir')
        mkdirp(self.directory)

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

        # Lua script with long shebang
        self.lua_shebang = os.path.join(self.tempdir, 'lua')
        with open(self.lua_shebang, 'w') as f:
            f.write(lua_line)
            f.write(last_line)

        # Lua script with long shebang
        self.lua_textbang = os.path.join(self.tempdir, 'lua_in_text')
        with open(self.lua_textbang, 'w') as f:
            f.write(short_line)
            f.write(lua_in_text)
            f.write(last_line)

        # Node script with long shebang
        self.node_shebang = os.path.join(self.tempdir, 'node')
        with open(self.node_shebang, 'w') as f:
            f.write(node_line)
            f.write(last_line)

        # Node script with long shebang
        self.node_textbang = os.path.join(self.tempdir, 'node_in_text')
        with open(self.node_textbang, 'w') as f:
            f.write(short_line)
            f.write(node_in_text)
            f.write(last_line)

        # Script already using sbang.
        self.has_sbang = os.path.join(self.tempdir, 'shebang')
        with open(self.has_sbang, 'w') as f:
            f.write(sbang_line)
            f.write(long_line)
            f.write(last_line)

        # Fake binary file.
        self.binary = os.path.join(self.tempdir, 'binary')
        tar = which('tar', required=True)
        tar('czf', self.binary, self.has_sbang)

    def destroy(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)


@pytest.fixture
def script_dir():
    sdir = ScriptDirectory()
    yield sdir
    sdir.destroy()


def test_shebang_handling(script_dir):
    assert shebang_too_long(script_dir.lua_shebang)
    assert shebang_too_long(script_dir.long_shebang)

    assert not shebang_too_long(script_dir.short_shebang)
    assert not shebang_too_long(script_dir.has_sbang)
    assert not shebang_too_long(script_dir.binary)
    assert not shebang_too_long(script_dir.directory)

    filter_shebangs_in_directory(script_dir.tempdir)

    # Make sure this is untouched
    with open(script_dir.short_shebang, 'r') as f:
        assert f.readline() == short_line
        assert f.readline() == last_line

    # Make sure this got patched.
    with open(script_dir.long_shebang, 'r') as f:
        assert f.readline() == sbang_line
        assert f.readline() == long_line
        assert f.readline() == last_line

    # Make sure this got patched.
    with open(script_dir.lua_shebang, 'r') as f:
        assert f.readline() == sbang_line
        assert f.readline() == lua_line_patched
        assert f.readline() == last_line

    # Make sure this got patched.
    with open(script_dir.node_shebang, 'r') as f:
        assert f.readline() == sbang_line
        assert f.readline() == node_line_patched
        assert f.readline() == last_line

    assert filecmp.cmp(script_dir.lua_textbang,
                       os.path.join(script_dir.tempdir, 'lua_in_text'))
    assert filecmp.cmp(script_dir.node_textbang,
                       os.path.join(script_dir.tempdir, 'node_in_text'))

    # Make sure this is untouched
    with open(script_dir.has_sbang, 'r') as f:
        assert f.readline() == sbang_line
        assert f.readline() == long_line
        assert f.readline() == last_line


def test_shebang_handles_non_writable_files(script_dir):
    # make a file non-writable
    st = os.stat(script_dir.long_shebang)
    not_writable_mode = st.st_mode & ~stat.S_IWRITE
    os.chmod(script_dir.long_shebang, not_writable_mode)

    test_shebang_handling(script_dir)

    st = os.stat(script_dir.long_shebang)
    assert oct(not_writable_mode) == oct(st.st_mode)
