# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import base64
import hashlib
import os
import re
import shutil
import sys

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.error
import spack.paths
import spack.util.prefix
import spack.util.spack_json as sjson
from spack.spec import Spec

test_suite_filename = 'test_suite.lock'
results_filename = 'results.txt'


def get_escaped_text_output(filename):
    """Retrieve and escape the expected text output from the file

    Args:
        filename (str): path to the file

    Returns:
        list: escaped text lines read from the file
    """
    with open(filename, 'r') as f:
        # Ensure special characters are escaped as needed
        expected = f.read()

    # Split the lines to make it easier to debug failures when there is
    # a lot of output
    return [re.escape(ln) for ln in expected.split('\n')]


def get_test_stage_dir():
    return spack.util.path.canonicalize_path(
        spack.config.get('config:test_stage', spack.paths.default_test_path)
    )


def get_all_test_suites():
    stage_root = get_test_stage_dir()
    if not os.path.isdir(stage_root):
        return []

    def valid_stage(d):
        dirpath = os.path.join(stage_root, d)
        return (os.path.isdir(dirpath) and
                test_suite_filename in os.listdir(dirpath))

    candidates = [
        os.path.join(stage_root, d, test_suite_filename)
        for d in os.listdir(stage_root)
        if valid_stage(d)
    ]

    test_suites = [TestSuite.from_file(c) for c in candidates]
    return test_suites


def get_named_test_suites(name):
    """Return a list of the names of any test suites with that name."""
    if not name:
        raise TestSuiteNameError('Test suite name is required.')

    test_suites = get_all_test_suites()
    return [ts for ts in test_suites if ts.name == name]


def get_test_suite(name):
    names = get_named_test_suites(name)
    if len(names) > 1:
        raise TestSuiteNameError(
            'Too many suites named "{0}".  May shadow hash.'.format(name)
        )

    if not names:
        return None
    return names[0]


def write_test_suite_file(suite):
    """Write the test suite to its lock file."""
    with open(suite.stage.join(test_suite_filename), 'w') as f:
        sjson.dump(suite.to_dict(), stream=f)


class TestSuite(object):
    def __init__(self, specs, alias=None):
        # copy so that different test suites have different package objects
        # even if they contain the same spec
        self.specs = [spec.copy() for spec in specs]
        self.current_test_spec = None  # spec currently tested, can be virtual
        self.current_base_spec = None  # spec currently running do_test

        self.alias = alias
        self._hash = None

        self.fails = 0

    @property
    def name(self):
        return self.alias if self.alias else self.content_hash

    @property
    def content_hash(self):
        if not self._hash:
            json_text = sjson.dump(self.to_dict())
            sha = hashlib.sha1(json_text.encode('utf-8'))
            b32_hash = base64.b32encode(sha.digest()).lower()
            if sys.version_info[0] >= 3:
                b32_hash = b32_hash.decode('utf-8')
            self._hash = b32_hash
        return self._hash

    def __call__(self, *args, **kwargs):
        self.write_reproducibility_data()

        remove_directory = kwargs.get('remove_directory', True)
        dirty = kwargs.get('dirty', False)
        fail_first = kwargs.get('fail_first', False)

        for spec in self.specs:
            try:
                if spec.package.test_suite:
                    raise TestSuiteSpecError(
                        "Package {0} cannot be run in two test suites at once"
                        .format(spec.package.name)
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
                spec.package.do_test(
                    dirty=dirty
                )

                # Clean up on success
                if remove_directory:
                    shutil.rmtree(test_dir)

                # Log test status based on whether any non-pass-only test
                # functions were called
                tested = os.path.exists(self.tested_file_for_spec(spec))
                status = 'PASSED' if tested else 'NO-TESTS'
                self.write_test_result(spec, status)
            except BaseException as exc:
                self.fails += 1
                if isinstance(exc, (SyntaxError, TestSuiteSpecError)):
                    # Create the test log file and report the error.
                    self.ensure_stage()
                    msg = 'Testing package {0}\n{1}'\
                        .format(self.test_pkg_id(spec), str(exc))
                    _add_msg_to_file(self.log_file_for_spec(spec), msg)

                self.write_test_result(spec, 'FAILED')
                if fail_first:
                    break
            finally:
                spec.package.test_suite = None
                self.current_test_spec = None
                self.current_base_spec = None

        if self.fails:
            raise TestSuiteFailure(self.fails)

    def ensure_stage(self):
        if not os.path.exists(self.stage):
            fs.mkdirp(self.stage)

    @property
    def stage(self):
        return spack.util.prefix.Prefix(
            os.path.join(get_test_stage_dir(), self.content_hash))

    @property
    def results_file(self):
        return self.stage.join(results_filename)

    @classmethod
    def test_pkg_id(cls, spec):
        """Build the standard install test package identifier

        Args:
        spec (Spec): instance of the spec under test

        Returns:
        (str): the install test package identifier
        """
        return spec.format('{name}-{version}-{hash:7}')

    @classmethod
    def test_log_name(cls, spec):
        return '%s-test-out.txt' % cls.test_pkg_id(spec)

    def log_file_for_spec(self, spec):
        return self.stage.join(self.test_log_name(spec))

    def test_dir_for_spec(self, spec):
        return self.stage.join(self.test_pkg_id(spec))

    @classmethod
    def tested_file_name(cls, spec):
        return '%s-tested.txt' % cls.test_pkg_id(spec)

    def tested_file_for_spec(self, spec):
        return self.stage.join(self.tested_file_name(spec))

    @property
    def current_test_cache_dir(self):
        if not (self.current_test_spec and self.current_base_spec):
            raise TestSuiteSpecError(
                "Unknown test cache directory: no specs being tested"
            )

        test_spec = self.current_test_spec
        base_spec = self.current_base_spec
        return self.test_dir_for_spec(base_spec).cache.join(test_spec.name)

    @property
    def current_test_data_dir(self):
        if not (self.current_test_spec and self.current_base_spec):
            raise TestSuiteSpecError(
                "Unknown test data directory: no specs being tested"
            )

        test_spec = self.current_test_spec
        base_spec = self.current_base_spec
        return self.test_dir_for_spec(base_spec).data.join(test_spec.name)

    def add_failure(self, exc, msg):
        current_hash = self.current_base_spec.dag_hash()
        current_failures = self.failures.get(current_hash, [])
        current_failures.append((exc, msg))
        self.failures[current_hash] = current_failures

    def write_test_result(self, spec, result):
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
        specs = [s.to_dict() for s in self.specs]
        d = {'specs': specs}
        if self.alias:
            d['alias'] = self.alias
        return d

    @staticmethod
    def from_dict(d):
        specs = [Spec.from_dict(spec_dict) for spec_dict in d['specs']]
        alias = d.get('alias', None)
        return TestSuite(specs, alias)

    @staticmethod
    def from_file(filename):
        try:
            with open(filename, 'r') as f:
                data = sjson.load(f)
                return TestSuite.from_dict(data)
        except Exception as e:
            tty.debug(e)
            raise sjson.SpackJSONError("error parsing JSON TestSuite:", str(e))


def _add_msg_to_file(filename, msg):
    """Add the message to the specified file

    Args:
        filename (str): path to the file
        msg (str): message to be appended to the file
    """
    with open(filename, 'a+') as f:
        f.write('{0}\n'.format(msg))


class TestFailure(spack.error.SpackError):
    """Raised when package tests have failed for an installation."""
    def __init__(self, failures):
        # Failures are all exceptions
        msg = "%d tests failed.\n" % len(failures)
        for failure, message in failures:
            msg += '\n\n%s\n' % str(failure)
            msg += '\n%s\n' % message

        super(TestFailure, self).__init__(msg)


class TestSuiteFailure(spack.error.SpackError):
    """Raised when one or more tests in a suite have failed."""
    def __init__(self, num_failures):
        msg = "%d test(s) in the suite failed.\n" % num_failures

        super(TestSuiteFailure, self).__init__(msg)


class TestSuiteSpecError(spack.error.SpackError):
    """Raised when there is an issue associated with the spec being tested."""


class TestSuiteNameError(spack.error.SpackError):
    """Raised when there is an issue with the naming of the test suite."""
