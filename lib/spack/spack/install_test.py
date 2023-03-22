# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import base64
import contextlib
import enum
import hashlib
import inspect
import io
import os
import re
import shutil
import sys
from collections import Counter
from typing import Callable, List, Optional, Tuple, Union

import llnl.util.filesystem as fs
import llnl.util.tty as tty
from llnl.util.lang import nullcontext
from llnl.util.tty.color import colorize

import spack.error
import spack.paths
import spack.util.spack_json as sjson
from spack.spec import Spec
from spack.util.prefix import Prefix
from spack.util.string import plural

#: Stand-alone test failure info type
TEST_FAILURE_TYPE = Tuple[BaseException, str]

#: Name of the test suite's (JSON) lock file
test_suite_filename = "test_suite.lock"

#: Name of the test suite results (summary) file
results_filename = "results.txt"

#: Name of the Spack install phase-time test log file
spack_install_test_log = "install-time-test-log.txt"


ListOrStringType = Union[str, List[str]]
SpecType = List[Spec]


@enum.unique
class TestStatus(enum.Enum):
    """Names of different stand-alone test states."""

    NO_TESTS = -1
    SKIPPED = 0
    FAILED = 1
    PASSED = 2

    def __str__(self):
        return f"{self.name}"

    def lower(self):
        name = f"{self.name}"
        return name.lower()


def get_escaped_text_output(filename):
    """Retrieve and escape the expected text output from the file

    Args:
        filename (str): path to the file

    Returns:
        list: escaped text lines read from the file
    """
    with open(filename, "r") as f:
        # Ensure special characters are escaped as needed
        expected = f.read()

    # Split the lines to make it easier to debug failures when there is
    # a lot of output
    return [re.escape(ln) for ln in expected.split("\n")]


def get_test_stage_dir():
    """Retrieves the ``config:test_stage`` path to the configured test stage
    root directory

    Returns:
        str: absolute path to the configured test stage root or, if none,
            the default test stage path
    """
    return spack.util.path.canonicalize_path(
        spack.config.get("config:test_stage", spack.paths.default_test_path)
    )


def cache_extra_test_sources(pkg: "spack.package_base.PackageBase", srcs: ListOrStringType):
    """Copy relative source paths to the corresponding install test subdir

    This routine is intended as an optional install test setup helper for
    grabbing source files/directories during the installation process and
    copying them to the installation test subdirectory for subsequent use
    during install testing.

    Args:
        pkg: package being tested
        srcs: relative path for file(s) and or subdirectory(ies) located in
            the staged source path that are to be copied to the corresponding
            location(s) under the install testing directory.
    """
    paths = [srcs] if isinstance(srcs, str) else srcs

    for path in paths:
        src_path = os.path.join(pkg.stage.source_path, path)
        dest_path = os.path.join(install_test_root(pkg), path)
        if os.path.isdir(src_path):
            fs.install_tree(src_path, dest_path)
        else:
            fs.mkdirp(os.path.dirname(dest_path))
            fs.copy(src_path, dest_path)


def check_outputs(expected: Union[list, set, str], actual: str):
    """Ensure the expected outputs are contained in the actual outputs.

    Args:
        expected: expected raw output string(s)
        actual: actual output string

    Raises:
        RuntimeError: the expected output is not found in the actual output
    """
    expected = expected if isinstance(expected, (list, set)) else [expected]
    for check in expected:
        if not re.search(check, actual):
            raise RuntimeError("Expected '{0}' in output '{1}'".format(check, actual))


def find_required_file(
    root: str, filename: str, expected: int = 1, recursive: bool = True
) -> ListOrStringType:
    """Find the required file(s) under the root directory.

    Args:
       root: root directory for the search
       filename: name of the file being located
       expected: expected number of files to be found under the directory
           (default is 1)
       recursive: ``True`` if subdirectories are to be searched, else ``False``
           (default is ``True``)

    Returns: the path(s), relative to root, to the required file(s)

    Raises:
        Exception: SkipTest when number of files detected does not match expected
    """
    paths = fs.find(root, filename, recursive=recursive)
    num_paths = len(paths)
    if num_paths != expected:
        files = ": {0}".format(", ".join(paths)) if num_paths else ""
        raise SkipTest(
            "Expected {0} of {1} under {2} but {3} found{4}".format(
                plural(expected, "copy", "copies"),
                filename,
                root,
                plural(num_paths, "copy", "copies"),
                files,
            )
        )

    return paths[0] if expected == 1 else paths


def install_test_root(pkg: "spack.package_base.PackageBase"):
    """The install test root directory.

    Args:
        pkg: package being tested
    """
    return os.path.join(pkg.metadata_dir, "test")


LogType = Union["tty.log.nixlog", "tty.log.winlog"]


def print_message(logger: LogType, msg: str, verbose: bool = False):
    """Print the message to the log, optionally echoing.

    Args:
        logger: instance of the output logger (e.g. nixlog or winlog)
        msg: message being output
        verbose: ``True`` displays verbose output, ``False`` suppresses
            it (``False`` is default)
    """
    if verbose:
        with logger.force_echo():
            tty.info(msg, format="g")
    else:
        tty.info(msg, format="g")


class PackageTest(object):
    """The class that manages stand-alone (post-install) package tests."""

    def __init__(self, pkg: "spack.package_base.PackageBase"):
        """
        Args:
            pkg: package being tested

        Raises:
            ValueError: if the package is not concrete
        """
        if not pkg.spec.concrete:
            raise ValueError("Stand-alone tests require a concrete package")

        self.counts: "Counter" = Counter()  # type: ignore[attr-defined]
        self.pkg = pkg
        self.test_failures: List[TEST_FAILURE_TYPE] = []
        self.test_parts: List[Tuple[str, "TestStatus"]] = []
        self.test_log_file: str
        self.pkg_id: str

        if pkg.test_suite:
            self.test_log_file = pkg.test_suite.log_file_for_spec(pkg.spec)
            self.tested_file = pkg.test_suite.tested_file_for_spec(pkg.spec)
            self.pkg_id = pkg.test_suite.test_pkg_id(pkg.spec)
        else:
            self.test_log_file = fs.join_path(pkg.stage.path, spack_install_test_log)
            self.pkg_id = pkg.spec.format("{name}-{version}-{hash:7}")

        fs.touch(self.test_log_file)  # Otherwise log_parse complains
        fs.set_install_permissions(self.test_log_file)

        # Internal logger for test part processing
        self._logger = None

    @property
    def logger(self) -> object:
        """The current logger or, if none, sets to one."""
        if not self._logger:
            self._logger = tty.log.log_output(self.test_log_file)

        return self._logger

    @contextlib.contextmanager
    def test_logger(self, verbose: bool, externals: bool):
        """Context manager for setting up the test logger

        Args:
            verbose: Display verbose output, including echoing to stdout,
                otherwise suppress it
            externals: ``True`` for performing tests if external package,
                ``False`` to skip them
        """
        with tty.log.log_output(self.test_log_file, verbose) as logger:
            with logger.force_echo():
                tty.msg("Testing package " + colorize(r"@*g{" + self.pkg_id + r"}"))

            # use debug print levels for log file to record commands
            old_debug = tty.is_debug()
            tty.set_debug(True)

            try:
                self._logger = logger
                yield logger
            finally:
                # reset debug level
                tty.set_debug(old_debug)

    @property
    def archived_install_test_log(self) -> str:
        return fs.join_path(self.pkg.metadata_dir, spack_install_test_log)

    def archive_install_test_log(self, dest_dir: str):
        if os.path.exists(self.test_log_file):
            fs.install(self.test_log_file, self.archived_install_test_log)

    def add_failure(self, exception: Exception, msg: str):
        """Add the failure details to the current list."""
        self.test_failures.append((exception, msg))

    def status(self, name: Optional[str], status: "TestStatus"):
        """Log the test status for the part name."""
        extra = "::{0}".format(name) if name else ""
        part_name = "{0}{1}".format(self.pkg.__class__.__name__, extra)
        self.test_parts.append((part_name, status))
        self.counts[status] += 1

    def phase_tests(
        self, builder: spack.builder.Builder, phase_name: str, method_names: List[str]
    ):
        """Execute the builder's package phase-time tests.

        Args:
            builder: builder for package being tested
            phase_name: the name of the build-time phase (e.g., ``build``, ``install``)
            method_names: phase-specific callback method names
        """
        verbose = tty.is_verbose()
        fail_fast = spack.config.get("config:fail_fast", False)

        with self.test_logger(verbose=verbose, externals=False) as logger:
            # Report running each of the methods in the build log
            print_message(logger, "Running {0}-time tests".format(phase_name), verbose)
            builder.pkg.test_suite.current_test_spec = builder.pkg.spec
            builder.pkg.test_suite.current_base_spec = builder.pkg.spec

            have_tests = any(name.startswith("test") for name in method_names)
            if have_tests:
                copy_test_files(builder.pkg, builder.pkg.spec)

            for name in method_names:
                try:
                    fn = getattr(builder, name)

                    msg = "RUN-TESTS: {0}-time tests [{1}]".format(phase_name, name)
                    print_message(logger, msg, verbose)

                    fn()

                # TODO/TBD: Do we want to treat these calls as test parts?
                except AttributeError as e:
                    msg = "RUN-TESTS: method not implemented [{0}]".format(name)
                    print_message(logger, msg, verbose)

                    self.add_failure(e, msg)
                    if fail_fast:
                        break

            if have_tests:
                print_message(logger, "Completed testing", verbose)

            # Raise any collected failures here
            if self.test_failures:
                raise TestFailure(self.test_failures)

    def stand_alone_tests(self, kwargs):
        """Run the package's stand-alone tests.

        Args:
            kwargs (dict): arguments to be used by the test process
        """
        import spack.build_environment

        spack.build_environment.start_build_process(self.pkg, test_process, kwargs)

    def parts(self) -> int:
        """The total number of (checked) test parts."""
        try:
            # New in Python 3.10
            total = self.counts.total()  # type: ignore[attr-defined]
        except AttributeError:
            nums = [n for _, n in self.counts.items()]
            total = sum(nums)
        return total

    def print_log_path(self):
        """Print the test log file location and, optionally, contents"""
        log = self.archived_install_test_log
        if not os.path.isfile(log):
            log = self.test_log_file
            if not (log and os.path.isfile(log)):
                tty.debug("There is no test log file (staged or installed)")
            return

        print("\nSee test results at:\n  {0}".format(log))

    def ran_tests(self) -> bool:
        """``True`` if ran tests, ``False`` otherwise."""
        return self.parts() > self.counts[TestStatus.NO_TESTS]

    def summarize(self):
        """Collect test results summary lines for this spec."""
        lines = []
        lines.append("{:=^80}".format(" SUMMARY: {0} ".format(self.pkg_id)))
        for name, status in self.test_parts:
            # TODO/TBD: Should the pkg_id be listed?  If so, remove above
            # msg = "{0}::{1} .. {2}\n".format(self.pkg_id, name, status)
            msg = "{0} .. {1}".format(name, status)
            lines.append(msg)

        summary = ["{0} {1}".format(n, s.lower()) for s, n in self.counts.items() if n > 0]
        totals = " {0} of {1} parts ".format(", ".join(summary), self.parts())
        lines.append("{:=^80}".format(totals))
        return lines


@contextlib.contextmanager
def test_part(
    pkg: "spack.package_base.PackageBase",
    test_name: str,
    purpose: str,
    work_dir: str = ".",
    verbose: bool = False,
):
    wdir = "." if work_dir is None else work_dir
    tester = pkg.tester
    # TODO: Replace "test" with "test_" when remove run_test, etc.
    assert test_name and test_name.startswith(
        "test"
    ), "Test name must start with 'test' but {0} was provided".format(test_name)

    if test_name == "test":
        tty.warn(
            "{0}: the 'test' method is deprecated. Convert stand-alone "
            "test(s) to methods with names starting 'test_'.".format(pkg.name)
        )

    title = "test: {0}: {1}".format(test_name, purpose or "")
    with fs.working_dir(wdir, create=True):
        try:
            status = TestStatus.PASSED
            context = tester.logger.force_echo if verbose else nullcontext
            with context():
                tty.info(title, format="g")
                yield
            print("{0}: {1}".format(status, test_name))
            tester.status(test_name, status)

        except SkipTest as e:
            status = TestStatus.SKIPPED
            print("{0}: {1}: {2}".format(status, test_name, e))
            tester.status(test_name, status)

        except (AssertionError, BaseException) as e:
            # print a summary of the error to the log file
            # so that cdash and junit reporters know about it
            exc_type, _, tb = sys.exc_info()
            status = TestStatus.FAILED
            print("{0}: {1}: {2}".format(status, test_name, e))
            tester.status(test_name, status)

            import traceback

            # remove the current call frame to exclude the extract_stack
            # call from the error
            stack = traceback.extract_stack()[:-1]

            # Package files have a line added at import time, so we re-read
            # the file to make line numbers match. We have to subtract two
            # from the line number because the original line number is
            # inflated once by the import statement and the lines are
            # displaced one by the import statement.
            for i, entry in enumerate(stack):
                filename, lineno, function, text = entry
                if spack.repo.is_package_file(filename):
                    with open(filename, "r") as f:
                        lines = f.readlines()
                    new_lineno = lineno - 2
                    text = lines[new_lineno]
                    if isinstance(entry, tuple):
                        new_entry = (filename, new_lineno, function, text)
                        stack[i] = new_entry  # type: ignore[call-overload]
                    elif isinstance(entry, list):
                        stack[i][1] = new_lineno  # type: ignore[index]

            # Format and print the stack
            out = traceback.format_list(stack)
            for line in out:
                print(line.rstrip("\n"))

            if exc_type is spack.util.executable.ProcessError:
                iostr = io.StringIO()
                spack.build_environment.write_log_summary(
                    iostr, "test", tester.test_log_file, last=1
                )  # type: ignore[assignment]
                m = iostr.getvalue()
            else:
                # We're below the package context, so get context from
                # stack instead of from traceback.
                # The traceback is truncated here, so we can't use it to
                # traverse the stack.
                m = "\n".join(spack.build_environment.get_package_context(tb))

            exc = e  # e is deleted after this block

            # If we fail fast, raise another error
            if spack.config.get("config:fail_fast", False):
                raise TestFailure([(exc, m)])
            else:
                tester.add_failure(exc, m)


def test_phase_callbacks(builder: spack.builder.Builder, phase_name: str, method_names: List[str]):
    """Execute the builder's package phase-time tests.

    Args:
        builder: builder for package being tested
        phase_name: the name of the build-time phase (e.g., ``build``, ``install``)
        method_names: phase-specific callback method names
    """
    if not builder.pkg.run_tests or not method_names:
        return

    builder.pkg.tester.phase_tests(builder, phase_name, method_names)


def copy_test_files(pkg: "spack.package_base.PackageBase", test_spec: spack.spec.Spec):
    """Copy the spec's cached and custom test files to the test stage directory.

    Args:
        pkg: package being tested
        test_spec: spec being tested, where the spec may be virtual

    Raises:
        TestSuiteError: package must be part of an active test suite
    """
    if pkg is None or pkg.test_suite is None:
        base = "Cannot copy test files"
        msg = (
            "{0} without a package".format(base)
            if pkg is None
            else "{0}: {1}: test suite is missing".format(pkg.name, base)
        )
        raise TestSuiteError(msg)

    # copy installed test sources cache into test stage dir
    if test_spec.concrete:
        cache_source = install_test_root(test_spec.package)
        cache_dir = pkg.test_suite.current_test_cache_dir
        if os.path.isdir(cache_source) and not os.path.exists(cache_dir):
            fs.install_tree(cache_source, cache_dir)

    # copy test data into test stage data dir
    try:
        pkg_cls = test_spec.package_class
    except spack.repo.UnknownPackageError:
        tty.debug(
            "{0}: skipping test data copy since no package class found".format(test_spec.name)
        )
        return

    package_dir = spack.package_base.package_directory(pkg_cls)
    data_source = Prefix(package_dir).test
    data_dir = pkg.test_suite.current_test_data_dir
    if os.path.isdir(data_source) and not os.path.exists(data_dir):
        # We assume data dir is used read-only
        # maybe enforce this later
        shutil.copytree(data_source, data_dir)


FunctionType = Union[str, Callable]
FunctionResult = List[FunctionType]


def test_functions(
    pkg: "spack.package_base.PackageBase", add_virtuals: bool = False, names: bool = False
) -> FunctionResult:
    """Grab all non-empty test functions.

    Args:
        pkg: package of interest
        add_virtuals: ``True`` adds test methods of provided package
            virtual, ``False`` only returns test functions of the package
        names: ``True`` returns test function names, ``False`` returns functions

    Returns: test functions or their names
    """
    pkg_cls = pkg.__class__
    classes = [pkg_cls]
    if add_virtuals:
        classes.extend([(Spec(name)).package_class for name in sorted(virtuals(pkg))])

    fmt = pkg_cls.name.lower() + ".{0}"
    tests = []
    for cls in classes:
        methods = inspect.getmembers(cls, predicate=lambda x: inspect.isfunction(x))
        for name, test_fn in methods:
            # TODO: Change to test_ once eliminate PackageBase.test()
            if not name.startswith("test"):
                continue

            # TBD: Remove empty method check once eliminate PackageBase.test()
            source = (inspect.getsource(test_fn)).splitlines()[1:]
            lines = [ln.strip() for ln in source if not ln.strip().startswith("#")]
            if len(lines) > 0 and lines[0] == "pass":
                continue

            tests.append(fmt.format(name) if names else test_fn)

    return tests


def test_parts_process(
    pkg: "spack.package_base.PackageBase", test_specs: List[spack.spec.Spec], verbose: bool = False
):
    """Process test parts associated with the package.

    Args:
        pkg: package being tested
        test_specs: list of test specs
        verbose: Display verbose output (suppress by default)

    Raises:
        TestSuiteError: package must be part of an active test suite
    """
    if pkg is None or pkg.test_suite is None:
        base = "Cannot process tests"
        msg = (
            "{0} without a package".format(base)
            if pkg is None
            else "{0}: {1}: test suite is missing".format(pkg.name, base)
        )
        raise TestSuiteError(msg)

    test_suite = pkg.test_suite
    tester = pkg.tester
    try:
        work_dir = test_suite.test_dir_for_spec(pkg.spec)
        for spec in test_specs:
            test_suite.current_test_spec = spec

            # grab test functions associated with the spec, which may be a
            # virtual spec
            tests = test_functions(spec.package_class, names=False)
            if len(tests) == 0:
                tester.status("", TestStatus.NO_TESTS)
                continue

            # copy custom and cached test files to the test stage directory
            copy_test_files(pkg, spec)

            # Run the tests
            for test_fn in tests:
                with test_part(
                    pkg,
                    test_fn.__name__,
                    purpose=getattr(test_fn, "__doc__"),
                    work_dir=work_dir,
                    verbose=verbose,
                ):
                    test_fn(pkg)

        # If fail-fast was on, we error out above
        # If we collect errors, raise them in batch here
        if tester.test_failures:
            raise TestFailure(tester.test_failures)

    finally:
        if tester.ran_tests():
            fs.touch(tester.tested_file)

            # log one more test message to provide a completion timestamp
            # for CDash reporting
            tty.msg("Completed testing")

            lines = tester.summarize()
            tty.msg("\n{0}".format("\n".join(lines)))

            if tester.test_failures:
                # Print the test log file path
                tty.msg("\n\nSee test results at:\n  {0}".format(tester.test_log_file))
        else:
            tty.msg("No tests to run")


def test_process(pkg: "spack.package_base.PackageBase", kwargs):
    verbose = kwargs.get("verbose", True)
    externals = kwargs.get("externals", False)

    with pkg.tester.test_logger(verbose, externals) as logger:
        if pkg.spec.external and not externals:
            print_message(logger, "Skipped tests for external package", verbose)
            pkg.tester.status(pkg.spec.name, TestStatus.SKIPPED)
            return

        if not pkg.spec.installed:
            print_message(logger, "Skipped not installed package", verbose)
            pkg.tester.status(pkg.spec.name, TestStatus.SKIPPED)
            return

        # run test methods from the package and all virtuals it provides
        v_names = virtuals(pkg)
        test_specs = [pkg.spec] + [spack.spec.Spec(v_name) for v_name in sorted(v_names)]
        test_parts_process(pkg, test_specs, verbose)


def virtuals(pkg):
    """Return a list of unique virtuals for the package.

    Args:
        pkg: package of interest

    Returns: names of unique virtual packages
    """
    # provided virtuals have to be deduped by name
    v_names = list(set([vspec.name for vspec in pkg.virtuals_provided]))

    # hack for compilers that are not dependencies (yet)
    # TODO: this all eventually goes away
    c_names = ("gcc", "intel", "intel-parallel-studio", "pgi")
    if pkg.name in c_names:
        v_names.extend(["c", "cxx", "fortran"])
    if pkg.spec.satisfies("llvm+clang"):
        v_names.extend(["c", "cxx"])
    return v_names


def get_all_test_suites():
    """Retrieves all validly staged TestSuites

    Returns:
        list: a list of TestSuite objects, which may be empty if there are none
    """
    stage_root = get_test_stage_dir()
    if not os.path.isdir(stage_root):
        return []

    def valid_stage(d):
        dirpath = os.path.join(stage_root, d)
        return os.path.isdir(dirpath) and test_suite_filename in os.listdir(dirpath)

    candidates = [
        os.path.join(stage_root, d, test_suite_filename)
        for d in os.listdir(stage_root)
        if valid_stage(d)
    ]

    test_suites = [TestSuite.from_file(c) for c in candidates]
    return test_suites


def get_named_test_suites(name):
    """Retrieves test suites with the provided name.

    Returns:
        list: a list of matching TestSuite instances, which may be empty if none

    Raises:
        Exception: TestSuiteNameError if no name is provided
    """
    if not name:
        raise TestSuiteNameError("Test suite name is required.")

    test_suites = get_all_test_suites()
    return [ts for ts in test_suites if ts.name == name]


def get_test_suite(name: str) -> Optional["TestSuite"]:
    """Ensure there is only one matching test suite with the provided name.

    Returns:
        the name if one matching test suite, else None

    Raises:
        TestSuiteNameError: If there are more than one matching TestSuites
    """
    suites = get_named_test_suites(name)
    if len(suites) > 1:
        raise TestSuiteNameError("Too many suites named '{0}'. May shadow hash.".format(name))

    if not suites:
        return None
    return suites[0]


def write_test_suite_file(suite):
    """Write the test suite to its (JSON) lock file."""
    with open(suite.stage.join(test_suite_filename), "w") as f:
        sjson.dump(suite.to_dict(), stream=f)


def write_test_summary(counts: "Counter"):
    """Write summary of the totals for each relevant status category.

    Args:
        counts: counts of the occurrences of relevant test status types
    """
    summary = ["{0} {1}".format(n, s.lower()) for s, n in counts.items() if n > 0]
    try:
        # New in Python 3.10
        total = counts.total()  # type: ignore[attr-defined]
    except AttributeError:
        nums = [n for _, n in counts.items()]
        total = sum(nums)

    if total:
        print("{:=^80}".format(" {0} of {1} ".format(", ".join(summary), plural(total, "spec"))))


class TestSuite(object):
    """The class that manages specs for ``spack test run`` execution."""

    def __init__(self, specs, alias=None):
        # copy so that different test suites have different package objects
        # even if they contain the same spec
        self.specs = [spec.copy() for spec in specs]
        self.current_test_spec = None  # spec currently tested, can be virtual
        self.current_base_spec = None  # spec currently running do_test

        self.alias = alias
        self._hash = None
        self._stage = None

        self.counts: "Counter" = Counter()

    @property
    def name(self):
        """The name (alias or, if none, hash) of the test suite."""
        return self.alias if self.alias else self.content_hash

    @property
    def content_hash(self):
        """The hash used to uniquely identify the test suite."""
        if not self._hash:
            json_text = sjson.dump(self.to_dict())
            sha = hashlib.sha1(json_text.encode("utf-8"))
            b32_hash = base64.b32encode(sha.digest()).lower()
            b32_hash = b32_hash.decode("utf-8")
            self._hash = b32_hash
        return self._hash

    def __call__(self, *args, **kwargs):
        self.write_reproducibility_data()

        remove_directory = kwargs.get("remove_directory", True)
        dirty = kwargs.get("dirty", False)
        fail_first = kwargs.get("fail_first", False)
        externals = kwargs.get("externals", False)

        for spec in self.specs:
            try:
                if spec.package.test_suite:
                    raise TestSuiteSpecError(
                        "Package {0} cannot be run in two test suites at once".format(
                            spec.package.name
                        )
                    )

                # Set up the test suite to know which test is running
                spec.package.test_suite = self
                self.current_base_spec = spec
                self.current_test_spec = spec

                # setup per-test directory in the stage dir
                test_dir = self.test_dir_for_spec(spec)
                if os.path.exists(test_dir):
                    shutil.rmtree(test_dir)
                fs.mkdirp(test_dir)

                # run the package tests
                spec.package.do_test(dirty=dirty, externals=externals)

                # Clean up on success
                if remove_directory:
                    shutil.rmtree(test_dir)

                # TBD: Should test parts be written and extracted from tested file?
                tested = os.path.exists(self.tested_file_for_spec(spec))
                if tested:
                    status = TestStatus.PASSED
                else:
                    self.ensure_stage()
                    if spec.external and not externals:
                        status = TestStatus.SKIPPED
                    elif not spec.installed:
                        status = TestStatus.SKIPPED
                    else:
                        status = TestStatus.NO_TESTS
                self.counts[status] += 1

                self.write_test_result(spec, status)
            except BaseException as exc:
                status = TestStatus.FAILED
                self.counts[status] += 1
                tty.debug("Test failure: {0}".format(str(exc)))

                if isinstance(exc, (SyntaxError, TestSuiteSpecError)):
                    # Create the test log file and report the error.
                    self.ensure_stage()
                    msg = "Testing package {0}\n{1}".format(self.test_pkg_id(spec), str(exc))
                    _add_msg_to_file(self.log_file_for_spec(spec), msg)

                msg = "Test failure: {0}".format(str(exc))
                _add_msg_to_file(self.log_file_for_spec(spec), msg)
                self.write_test_result(spec, TestStatus.FAILED)
                if fail_first:
                    break

            finally:
                spec.package.test_suite = None
                self.current_test_spec = None
                self.current_base_spec = None

        write_test_summary(self.counts)

        if self.counts[TestStatus.FAILED]:
            for spec in self.specs:
                print(
                    "\nSee {0} test results at:\n  {1}".format(
                        spec.format("{name}-{version}-{hash:7}"), self.log_file_for_spec(spec)
                    )
                )

        failures = self.counts[TestStatus.FAILED]
        if failures:
            raise TestSuiteFailure(failures)

    def ensure_stage(self):
        """Ensure the test suite stage directory exists."""
        if not os.path.exists(self.stage):
            fs.mkdirp(self.stage)

    @property
    def stage(self):
        """The root test suite stage directory.

        Returns:
            str: the spec's test stage directory path
        """
        if not self._stage:
            self._stage = Prefix(fs.join_path(get_test_stage_dir(), self.content_hash))
        return self._stage

    @stage.setter
    def stage(self, value):
        """Set the value of a non-default stage directory."""
        self._stage = value if isinstance(value, Prefix) else Prefix(value)

    @property
    def results_file(self):
        """The path to the results summary file."""
        return self.stage.join(results_filename)

    @classmethod
    def test_pkg_id(cls, spec):
        """The standard install test package identifier.

        Args:
            spec: instance of the spec under test

        Returns:
            str: the install test package identifier
        """
        return spec.format("{name}-{version}-{hash:7}")

    @classmethod
    def test_log_name(cls, spec):
        """The standard log filename for a spec.

        Args:
            spec (spack.spec.Spec): instance of the spec under test

        Returns:
            str: the spec's log filename
        """
        return "%s-test-out.txt" % cls.test_pkg_id(spec)

    def log_file_for_spec(self, spec):
        """The test log file path for the provided spec.

        Args:
            spec (spack.spec.Spec): instance of the spec under test

        Returns:
            str: the path to the spec's log file
        """
        return self.stage.join(self.test_log_name(spec))

    def test_dir_for_spec(self, spec):
        """The path to the test stage directory for the provided spec.

        Args:
            spec (spack.spec.Spec): instance of the spec under test

        Returns:
            str: the spec's test stage directory path
        """
        return Prefix(self.stage.join(self.test_pkg_id(spec)))

    @classmethod
    def tested_file_name(cls, spec):
        """The standard test status filename for the spec.

        Args:
            spec (spack.spec.Spec): instance of the spec under test

        Returns:
            str: the spec's test status filename
        """
        return "%s-tested.txt" % cls.test_pkg_id(spec)

    def tested_file_for_spec(self, spec):
        """The test status file path for the spec.

        Args:
            spec (spack.spec.Spec): instance of the spec under test

        Returns:
            str: the spec's test status file path
        """
        return fs.join_path(self.stage, self.tested_file_name(spec))

    @property
    def current_test_cache_dir(self):
        """Path to the test stage directory where the current spec's cached
        build-time files were automatically copied.

        Returns:
            str: path to the current spec's staged, cached build-time files.

        Raises:
            TestSuiteSpecError: If there is no spec being tested
        """
        if not (self.current_test_spec and self.current_base_spec):
            raise TestSuiteSpecError("Unknown test cache directory: no specs being tested")

        test_spec = self.current_test_spec
        base_spec = self.current_base_spec
        return self.test_dir_for_spec(base_spec).cache.join(test_spec.name)

    @property
    def current_test_data_dir(self):
        """Path to the test stage directory where the current spec's custom
        package (data) files were automatically copied.

        Returns:
            str: path to the current spec's staged, custom package (data) files

        Raises:
            TestSuiteSpecError: If there is no spec being tested
        """
        if not (self.current_test_spec and self.current_base_spec):
            raise TestSuiteSpecError("Unknown test data directory: no specs being tested")

        test_spec = self.current_test_spec
        base_spec = self.current_base_spec
        return self.test_dir_for_spec(base_spec).data.join(test_spec.name)

    def write_test_result(self, spec, result):
        """Write the spec's test result to the test suite results file.

        Args:
            spec (spack.spec.Spec): instance of the spec under test
            result (str): result from the spec's test execution (e.g, PASSED)
        """
        msg = "{0} {1}".format(self.test_pkg_id(spec), result)
        _add_msg_to_file(self.results_file, msg)

    def write_reproducibility_data(self):
        for spec in self.specs:
            repo_cache_path = self.stage.repo.join(spec.name)
            spack.repo.path.dump_provenance(spec, repo_cache_path)
            for vspec in spec.package.virtuals_provided:
                repo_cache_path = self.stage.repo.join(vspec.name)
                if not os.path.exists(repo_cache_path):
                    try:
                        spack.repo.path.dump_provenance(vspec, repo_cache_path)
                    except spack.repo.UnknownPackageError:
                        pass  # not all virtuals have package files

        write_test_suite_file(self)

    def to_dict(self):
        """Build a dictionary for the test suite.

        Returns:
            dict: The dictionary contains entries for up to two keys:

                specs: list of the test suite's specs in dictionary form
                alias: the alias, or name, given to the test suite if provided
        """
        specs = [s.to_dict() for s in self.specs]
        d = {"specs": specs}
        if self.alias:
            d["alias"] = self.alias
        return d

    @staticmethod
    def from_dict(d):
        """Instantiates a TestSuite based on a dictionary specs and an
        optional alias:

            specs: list of the test suite's specs in dictionary form
            alias: the test suite alias

        Returns:
            TestSuite: Instance created from the specs
        """
        specs = [Spec.from_dict(spec_dict) for spec_dict in d["specs"]]
        alias = d.get("alias", None)
        return TestSuite(specs, alias)

    @staticmethod
    def from_file(filename):
        """Instantiate a TestSuite using the specs and optional alias
        provided in the given file.

        Args:
            filename (str): The path to the JSON file containing the test
                suite specs and optional alias.

        Raises:
            BaseException: sjson.SpackJSONError if problem parsing the file
        """
        try:
            with open(filename, "r") as f:
                data = sjson.load(f)
                test_suite = TestSuite.from_dict(data)
                content_hash = os.path.basename(os.path.dirname(filename))
                test_suite._hash = content_hash
                return test_suite
        except Exception as e:
            raise sjson.SpackJSONError("error parsing JSON TestSuite:", e)


def _add_msg_to_file(filename, msg):
    """Append the message to the specified file.

    Args:
        filename (str): path to the file
        msg (str): message to be appended to the file
    """
    with open(filename, "a+") as f:
        f.write("{0}\n".format(msg))


class SkipTest(spack.error.SpackError):
    """Raised when a test (part) is being skipped."""


class TestFailure(spack.error.SpackError):
    """Raised when package tests have failed for an installation."""

    def __init__(self, failures: List[TEST_FAILURE_TYPE]):
        # Failures are all exceptions
        num = len(failures)
        msg = "{0} failed.\n".format(plural(num, "test"))
        for failure, message in failures:
            msg += "\n\n%s\n" % str(failure)
            msg += "\n%s\n" % message

        super(TestFailure, self).__init__(msg)


class TestSuiteError(spack.error.SpackError):
    """Raised when there is an error with the test suite."""


class TestSuiteFailure(spack.error.SpackError):
    """Raised when one or more tests in a suite have failed."""

    def __init__(self, num_failures):
        msg = "%d test(s) in the suite failed.\n" % num_failures

        super(TestSuiteFailure, self).__init__(msg)


class TestSuiteSpecError(spack.error.SpackError):
    """Raised when there is an issue associated with the spec being tested."""


class TestSuiteNameError(spack.error.SpackError):
    """Raised when there is an issue with the naming of the test suite."""
