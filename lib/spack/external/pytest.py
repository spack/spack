# The MIT License (MIT)
#
# Copyright (c) 2004-2017 Holger Krekel and others
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# PYTHON_ARGCOMPLETE_OK
"""
pytest: unit and functional testing with Python.
"""


# else we are imported

from _pytest.config import (
    main, UsageError, _preloadplugins, cmdline,
    hookspec, hookimpl
)
from _pytest.fixtures import fixture, yield_fixture
from _pytest.assertion import register_assert_rewrite
from _pytest.freeze_support import freeze_includes
from _pytest import __version__
from _pytest.debugging import pytestPDB as __pytestPDB
from _pytest.recwarn import warns, deprecated_call
from _pytest.outcomes import fail, skip, importorskip, exit, xfail
from _pytest.mark import MARK_GEN as mark, param
from _pytest.main import Item, Collector, File, Session
from _pytest.fixtures import fillfixtures as _fillfuncargs
from _pytest.python import (
    Module, Class, Instance, Function, Generator,
)

from _pytest.python_api import approx, raises

set_trace = __pytestPDB.set_trace

__all__ = [
    'main',
    'UsageError',
    'cmdline',
    'hookspec',
    'hookimpl',
    '__version__',
    'register_assert_rewrite',
    'freeze_includes',
    'set_trace',
    'warns',
    'deprecated_call',
    'fixture',
    'yield_fixture',
    'fail',
    'skip',
    'xfail',
    'importorskip',
    'exit',
    'mark',
    'param',
    'approx',
    '_fillfuncargs',

    'Item',
    'File',
    'Collector',
    'Session',
    'Module',
    'Class',
    'Instance',
    'Function',
    'Generator',
    'raises',


]

if __name__ == '__main__':
    # if run as a script or by 'python -m pytest'
    # we trigger the below "else" condition by the following import
    import pytest
    raise SystemExit(pytest.main())
else:

    from _pytest.compat import _setup_collect_fakemodule
    _preloadplugins()  # to populate pytest.* namespace so help(pytest) works
    _setup_collect_fakemodule()
