# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib
import re
import subprocess
import sys
from datetime import datetime, timedelta

import pytest

import spack.util.lang
from spack.util.lang import (
    Singleton,
    SingletonInstantiationError,
    dedupe,
    match_predicate,
    memoized,
    pretty_date,
)


@pytest.fixture()
def now():
    return datetime.now()


@pytest.fixture()
def module_path(tmp_path: pathlib.Path):
    m = tmp_path / "foo.py"
    content = """
import os

value = 1
path = os.path.join('/usr', 'bin')
"""
    m.write_text(content)

    yield str(m)

    # Don't leave garbage in the module system
    if "foo" in sys.modules:
        del sys.modules["foo"]


def test_pretty_date():
    """Make sure pretty_date prints the right dates."""
    now = datetime.now()

    just_now = now - timedelta(seconds=5)
    assert pretty_date(just_now, now) == "just now"

    seconds = now - timedelta(seconds=30)
    assert pretty_date(seconds, now) == "30 seconds ago"

    a_minute = now - timedelta(seconds=60)
    assert pretty_date(a_minute, now) == "a minute ago"

    minutes = now - timedelta(seconds=1800)
    assert pretty_date(minutes, now) == "30 minutes ago"

    an_hour = now - timedelta(hours=1)
    assert pretty_date(an_hour, now) == "an hour ago"

    hours = now - timedelta(hours=2)
    assert pretty_date(hours, now) == "2 hours ago"

    yesterday = now - timedelta(days=1)
    assert pretty_date(yesterday, now) == "yesterday"

    days = now - timedelta(days=3)
    assert pretty_date(days, now) == "3 days ago"

    a_week = now - timedelta(weeks=1)
    assert pretty_date(a_week, now) == "a week ago"

    weeks = now - timedelta(weeks=2)
    assert pretty_date(weeks, now) == "2 weeks ago"

    a_month = now - timedelta(days=30)
    assert pretty_date(a_month, now) == "a month ago"

    months = now - timedelta(days=60)
    assert pretty_date(months, now) == "2 months ago"

    a_year = now - timedelta(days=365)
    assert pretty_date(a_year, now) == "a year ago"

    years = now - timedelta(days=365 * 2)
    assert pretty_date(years, now) == "2 years ago"


@pytest.mark.parametrize(
    "delta,pretty_string",
    [
        (timedelta(days=1), "a day ago"),
        (timedelta(days=1), "yesterday"),
        (timedelta(days=1), "1 day ago"),
        (timedelta(weeks=1), "1 week ago"),
        (timedelta(weeks=3), "3 weeks ago"),
        (timedelta(days=30), "1 month ago"),
        (timedelta(days=730), "2 years  ago"),
    ],
)
def test_pretty_string_to_date_delta(now, delta, pretty_string):
    t1 = now - delta
    t2 = spack.util.lang.pretty_string_to_date(pretty_string, now)
    assert t1 == t2


@pytest.mark.parametrize(
    "format,pretty_string",
    [
        ("%Y", "2018"),
        ("%Y-%m", "2015-03"),
        ("%Y-%m-%d", "2015-03-28"),
        ("%Y-%m-%d %H:%M", "2015-03-28 11:12"),
        ("%Y-%m-%d %H:%M:%S", "2015-03-28 23:34:45"),
    ],
)
def test_pretty_string_to_date(format, pretty_string):
    t1 = datetime.strptime(pretty_string, format)
    t2 = spack.util.lang.pretty_string_to_date(pretty_string, now)
    assert t1 == t2


def test_pretty_seconds():
    assert spack.util.lang.pretty_seconds(2.1) == "2.100s"
    assert spack.util.lang.pretty_seconds(2.1 / 1000) == "2.100ms"
    assert spack.util.lang.pretty_seconds(2.1 / 1000 / 1000) == "2.100us"
    assert spack.util.lang.pretty_seconds(2.1 / 1000 / 1000 / 1000) == "2.100ns"
    assert spack.util.lang.pretty_seconds(2.1 / 1000 / 1000 / 1000 / 10) == "0.210ns"


def test_pretty_duration():
    assert spack.util.lang.pretty_duration(0) == "0s"
    assert spack.util.lang.pretty_duration(45) == "45s"
    assert spack.util.lang.pretty_duration(60) == "1m00s"
    assert spack.util.lang.pretty_duration(125) == "2m05s"
    assert spack.util.lang.pretty_duration(3600) == "1h00m"
    assert spack.util.lang.pretty_duration(3661) == "1h01m"


def test_match_predicate():
    matcher = match_predicate(lambda x: True)
    assert matcher("foo")
    assert matcher("bar")
    assert matcher("baz")

    matcher = match_predicate(["foo", "bar"])
    assert matcher("foo")
    assert matcher("bar")
    assert not matcher("baz")

    matcher = match_predicate(r"^(foo|bar)$")
    assert matcher("foo")
    assert matcher("bar")
    assert not matcher("baz")

    with pytest.raises(ValueError):
        matcher = match_predicate(object())
        matcher("foo")


def test_load_modules_from_file(module_path):
    # Check prerequisites
    assert "foo" not in sys.modules

    # Check that the module is loaded correctly from file
    foo = spack.util.lang.load_module_from_file("foo", module_path)
    assert "foo" in sys.modules
    assert foo.value == 1
    assert foo.path == os.path.join("/usr", "bin")

    # Check that the module is not reloaded a second time on subsequent calls
    foo.value = 2
    foo = spack.util.lang.load_module_from_file("foo", module_path)
    assert "foo" in sys.modules
    assert foo.value == 2
    assert foo.path == os.path.join("/usr", "bin")


def test_uniq():
    assert [1, 2, 3] == spack.util.lang.uniq([1, 2, 3])
    assert [1, 2, 3] == spack.util.lang.uniq([1, 1, 1, 1, 2, 2, 2, 3, 3])
    assert [1, 2, 1] == spack.util.lang.uniq([1, 1, 1, 1, 2, 2, 2, 1, 1])
    assert [] == spack.util.lang.uniq([])


def test_key_ordering():
    """Ensure that key ordering works correctly."""

    with pytest.raises(TypeError):

        @spack.util.lang.key_ordering
        class ClassThatHasNoCmpKeyMethod:
            # this will raise b/c it does not define _cmp_key
            pass

    @spack.util.lang.key_ordering
    class KeyComparable:
        def __init__(self, t):
            self.t = t

        def _cmp_key(self):
            return self.t

    a = KeyComparable((1, 2, 3))
    a2 = KeyComparable((1, 2, 3))
    b = KeyComparable((2, 3, 4))
    b2 = KeyComparable((2, 3, 4))

    assert a == a
    assert a == a2
    assert a2 == a

    assert b == b
    assert b == b2
    assert b2 == b

    assert a != b

    assert a < b
    assert b > a

    assert a <= b
    assert b >= a

    assert a <= a
    assert a <= a2
    assert b >= b
    assert b >= b2

    assert hash(a) != hash(b)
    assert hash(a) == hash(a)
    assert hash(a) == hash(a2)
    assert hash(b) == hash(b)
    assert hash(b) == hash(b2)


@pytest.mark.parametrize("args, kwargs", [((1,), {}), ((), {"a": 3}), ((1,), {"a": 3})])
def test_memoized(args, kwargs):
    @memoized
    def f(*args, **kwargs):
        return "return-value"

    assert f(*args, **kwargs) == "return-value"
    assert f(*args, **kwargs) == "return-value"
    assert f.cache_info().hits == 1


@pytest.mark.parametrize("args, kwargs", [(([1],), {}), ((), {"a": [1]})])
def test_memoized_unhashable(args, kwargs):
    """Check that an exception is raised clearly"""

    @memoized
    def f(*args, **kwargs):
        return None

    with pytest.raises(TypeError, match="unhashable type:"):
        f(*args, **kwargs)


def test_dedupe():
    assert [x for x in dedupe([1, 2, 1, 3, 2])] == [1, 2, 3]
    assert [x for x in dedupe([1, -2, 1, 3, 2], key=abs)] == [1, -2, 3]


def test_grouped_exception():
    h = spack.util.lang.GroupedExceptionHandler()

    def inner():
        raise ValueError("wow!")

    with h.forward("inner method"):
        inner()

    with h.forward("top-level"):
        raise TypeError("ok")


def test_grouped_exception_base_type():
    h = spack.util.lang.GroupedExceptionHandler()

    with h.forward("catch-runtime-error", RuntimeError):
        raise NotImplementedError()

    with pytest.raises(NotImplementedError):
        with h.forward("catch-value-error", ValueError):
            raise NotImplementedError()

    message = h.grouped_message(with_tracebacks=False)
    assert "catch-runtime-error" in message
    assert "catch-value-error" not in message


def test_class_level_constant_value():
    """Tests that the Const descriptor does not allow overwriting the value from an instance"""

    class _SomeClass:
        CONST_VALUE = spack.util.lang.Const(10)

    with pytest.raises(TypeError, match="not support assignment"):
        _SomeClass().CONST_VALUE = 11


def test_deprecated_property():
    """Tests the behavior of the DeprecatedProperty descriptor, which is can be used when
    deprecating an attribute.
    """

    class _Deprecated(spack.util.lang.DeprecatedProperty):
        def factory(self, instance, owner):
            return 46

    class _SomeClass:
        deprecated = _Deprecated("deprecated")

    # Default behavior is to just return the deprecated value
    s = _SomeClass()
    assert s.deprecated == 46

    # When setting error_level to 1 the attribute warns
    _SomeClass.deprecated.error_lvl = 1
    with pytest.warns(UserWarning):
        assert s.deprecated == 46

    # When setting error_level to 2 an exception is raised
    _SomeClass.deprecated.error_lvl = 2
    with pytest.raises(AttributeError):
        _ = s.deprecated


def test_fnmatch_multiple():
    named_patterns = {"a": "libf*o.so", "b": "libb*r.so"}
    regex = re.compile(spack.util.lang.fnmatch_translate_multiple(named_patterns))

    a = regex.match("libfoo.so")
    assert a and a.group("a") == "libfoo.so"

    b = regex.match("libbar.so")
    assert b and b.group("b") == "libbar.so"

    assert not regex.match("libfoo.so.1")
    assert not regex.match("libbar.so.1")
    assert not regex.match("libfoo.solibbar.so")
    assert not regex.match("libbaz.so")


def _attr_error_factory():
    raise AttributeError("Could not make something")


def test_singleton_instantiation_attr_failure():
    """
    If an AttributeError occurs during the instantiation of a Singleton
    object, we want to see that error.
    """
    x = Singleton(_attr_error_factory)
    with pytest.raises(SingletonInstantiationError) as last_exception:
        x.something

    def follow_exceptions(e):
        while e:
            yield e
            e = e.__cause__ or e.__context__

    assert any(
        "Could not make something" in str(e) for e in follow_exceptions(last_exception.value)
    )


class TestPriorityOrderedMapping:
    @pytest.mark.parametrize(
        "elements,expected",
        [
            # Push out-of-order with explicit, and different, priorities
            ([("b", 2), ("a", 1), ("d", 4), ("c", 3)], ["a", "b", "c", "d"]),
            # Push in-order with priority=None
            ([("a", None), ("b", None), ("c", None), ("d", None)], ["a", "b", "c", "d"]),
            # Mix explicit and implicit priorities
            ([("b", 2), ("c", None), ("a", 1), ("d", None)], ["a", "b", "c", "d"]),
            ([("b", 10), ("c", None), ("a", -20), ("d", None)], ["a", "b", "c", "d"]),
            ([("b", 10), ("c", None), ("a", 20), ("d", None)], ["b", "c", "a", "d"]),
            # Adding the same key twice with different priorities
            ([("b", 10), ("c", None), ("a", 20), ("d", None), ("a", -20)], ["a", "b", "c", "d"]),
            # Adding the same key twice, no priorities
            ([("b", None), ("a", None), ("b", None)], ["a", "b"]),
        ],
    )
    def test_iteration_order(self, elements, expected):
        """Tests that the iteration order respects priorities, no matter the insertion order."""
        m = spack.util.lang.PriorityOrderedMapping()
        for key, priority in elements:
            m.add(key, value=None, priority=priority)
        assert list(m) == expected

    def test_reverse_iteration(self):
        """Tests that we can conveniently use reverse iteration"""
        m = spack.util.lang.PriorityOrderedMapping()
        for key, value in [("a", 1), ("b", 2), ("c", 3)]:
            m.add(key, value=value)

        assert list(m) == ["a", "b", "c"]
        assert list(reversed(m)) == ["c", "b", "a"]

        assert list(m.keys()) == ["a", "b", "c"]
        assert list(m.reversed_keys()) == ["c", "b", "a"]

        assert list(m.values()) == [1, 2, 3]
        assert list(m.reversed_values()) == [3, 2, 1]


def _run_in_pty(child_code: str, answer: bytes, tmp_path):
    """Run ``child_code`` in a Python subprocess whose controlling terminal is a fresh pty.

    The child's stdin, stdout and stderr are all redirected away from the terminal, as
    they are under fish's ``capture_all`` or ``$(...)`` capture; only the controlling
    terminal is the pty. ``answer`` is typed on the pty up front (type-ahead); the child
    reports through ``RESULT_FILE``. Returns ``(pty_output, result)``.
    """
    import pty

    result_file = tmp_path / "result"
    pid, fd = pty.fork()
    if pid == 0:  # child: runs under the pty, exits via os._exit
        proc = subprocess.run(
            [sys.executable, "-c", child_code],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "RESULT_FILE": str(result_file)},
        )
        if proc.returncode != 0:
            result_file.write_text("CHILD FAILED\n" + proc.stderr.decode(errors="replace"))
        os._exit(proc.returncode)

    os.write(fd, answer)
    output = b""
    while True:
        try:
            chunk = os.read(fd, 4096)
        except OSError:  # EIO once the child has closed the child side
            break
        if not chunk:
            break
        output += chunk
    os.waitpid(pid, 0)
    os.close(fd)
    return output.decode(errors="replace"), result_file.read_text()


_READLINE_CHILD = """
import os, sys
sys.path[:0] = {path!r}
import spack.util.lang as lang
with lang.open_controlling_terminal() as terminal:
    if terminal is None:
        result = "NO-TERMINAL"
    else:
        answer = lang.readline_with_timeout("Proceed? [y/N]", {timeout}, terminal=terminal)
        result = "ANSWER " + repr(answer)
# anything written to the captured streams would be lost on the user; make sure it is empty
open(os.environ["RESULT_FILE"], "w").write(result)
"""


@pytest.mark.not_on_windows("uses pty.fork")
@pytest.mark.parametrize(
    "typed,expected", [(b"y\r", "'y'"), (b"\r", "''"), (b"no\r", "'no'"), (b"yx\x7f\r", "'y'")]
)
def test_readline_with_timeout_on_controlling_terminal(typed, expected, tmp_path):
    """The prompt is shown and answered on the controlling terminal even when stdin,
    stdout and stderr are all redirected (fish's ``capture_all``, ``2>&1 | tee``)."""
    child = _READLINE_CHILD.format(path=sys.path, timeout=5)
    pty_out, result = _run_in_pty(child, typed, tmp_path)
    assert "Proceed? [y/N]" in pty_out, result
    assert result == f"ANSWER {expected}"


@pytest.mark.not_on_windows("uses pty.fork")
def test_readline_with_timeout_times_out(tmp_path):
    child = _READLINE_CHILD.format(path=sys.path, timeout=1)
    pty_out, result = _run_in_pty(child, b"", tmp_path)
    assert "Proceed? [y/N]" in pty_out, result
    assert result == "ANSWER None"


@pytest.mark.not_on_windows("uses pty.fork")
def test_open_controlling_terminal_background_job(tmp_path):
    """A process outside the terminal's foreground process group cannot prompt."""
    child = _READLINE_CHILD.format(path=sys.path, timeout=5).replace(
        "import spack.util.lang as lang", "os.setpgrp()\nimport spack.util.lang as lang"
    )
    pty_out, result = _run_in_pty(child, b"y\r", tmp_path)
    assert result == "NO-TERMINAL"
    assert "Proceed?" not in pty_out


def test_open_controlling_terminal_without_terminal(monkeypatch):
    """No controlling terminal (cron, CI, ``setsid``): yields None rather than raising."""
    if sys.platform == "win32":
        monkeypatch.setattr(sys, "stdin", None)
    else:
        real_open = os.open

        def no_tty(path, *args, **kwargs):
            if path == "/dev/tty":
                raise OSError(6, "Device not configured", path)
            return real_open(path, *args, **kwargs)

        monkeypatch.setattr(os, "open", no_tty)

    with spack.util.lang.open_controlling_terminal() as terminal:
        assert terminal is None
