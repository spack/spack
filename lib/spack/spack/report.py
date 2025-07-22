# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tools to produce reports of spec installations or tests"""
import collections
import gzip
import os
import time
import traceback

import spack.error

reporter = None
report_file = None

Property = collections.namedtuple("Property", ["name", "value"])


class Record(dict):
    """Data class that provides attr-style access to a dictionary

    Attributes beginning with ``_`` are reserved for the Record class itself."""

    def __getattr__(self, name):
        # only called if no attribute exists
        if name in self:
            return self[name]
        raise AttributeError(f"Record for {self.name} has no attribute {name}")

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self[name] = value


class RequestRecord(Record):
    """Data class for recording outcomes for an entire DAG

    Each BuildRequest in the installer and each root spec in a TestSuite generates a
    RequestRecord. The ``packages`` list of the RequestRecord is a list of SpecRecord
    objects recording individual data for each node in the Spec represented by the
    RequestRecord.

    These data classes are collated by the reporters in lib/spack/spack/reporters
    """

    def __init__(self, spec):
        super().__init__()
        self._spec = spec
        self.name = spec.name
        self.nerrors = None
        self.nfailures = None
        self.npackages = None
        self.time = None
        self.timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
        self.properties = [
            Property("architecture", spec.architecture),
            # Property("compiler", spec.compiler),
        ]
        self.packages = []

    def skip_installed(self):
        """Insert records for all nodes in the DAG that are no-ops for this request"""
        for dep in filter(lambda x: x.installed or x.external, self._spec.traverse()):
            record = InstallRecord(dep)
            record.skip(msg="Spec external or already installed")
            self.packages.append(record)

    def append_record(self, record):
        self.packages.append(record)

    def summarize(self):
        """Construct request-level summaries of the individual records"""
        self.npackages = len(self.packages)
        self.nfailures = len([r for r in self.packages if r.result == "failure"])
        self.nerrors = len([r for r in self.packages if r.result == "error"])
        self.time = sum(float(r.elapsed_time or 0.0) for r in self.packages)


class SpecRecord(Record):
    """Individual record for a single spec within a request"""

    def __init__(self, spec):
        super().__init__()
        self._spec = spec
        self._package = spec.package
        self._start_time = None
        self.name = spec.name
        self.id = spec.dag_hash()
        self.elapsed_time = None

    def start(self):
        self._start_time = time.time()

    def skip(self, msg):
        self.result = "skipped"
        self.elapsed_time = 0.0
        self.message = msg

    def fail(self, exc):
        """Record failure based on exception type

        Errors wrapped by spack.error.InstallError are "failures"
        Other exceptions are "errors".
        """
        if isinstance(exc, spack.error.InstallError):
            self.result = "failure"
            self.message = exc.message or "Installation failure"
            self.exception = exc.traceback
        else:
            self.result = "error"
            self.message = str(exc) or "Unknown error"
            self.exception = traceback.format_exc()
        self.stdout = self.fetch_log() + self.message
        assert self._start_time, "Start time is None"
        self.elapsed_time = time.time() - self._start_time

    def succeed(self):
        """Record success for this spec"""
        self.result = "success"
        self.stdout = self.fetch_log()
        assert self._start_time, "Start time is None"
        self.elapsed_time = time.time() - self._start_time


class InstallRecord(SpecRecord):
    """Record class with specialization for install logs."""

    def __init__(self, spec):
        super().__init__(spec)
        self.installed_from_binary_cache = None

    def fetch_log(self):
        """Install log comes from install prefix on success, or stage dir on failure."""
        try:
            if os.path.exists(self._package.install_log_path):
                stream = gzip.open(self._package.install_log_path, "rt", encoding="utf-8")
            else:
                stream = open(self._package.log_path, encoding="utf-8")
            with stream as f:
                return f.read()
        except OSError:
            return f"Cannot open log for {self._spec.cshort_spec}"

    def succeed(self):
        super().succeed()
        self.installed_from_binary_cache = self._package.installed_from_binary_cache


class TestRecord(SpecRecord):
    """Record class with specialization for test logs."""

    def __init__(self, spec, directory):
        super().__init__(spec)
        self.directory = directory

    def fetch_log(self):
        """Get output from test log"""
        log_file = os.path.join(self.directory, self._package.test_suite.test_log_name(self._spec))
        try:
            with open(log_file, "r", encoding="utf-8") as stream:
                return "".join(stream.readlines())
        except Exception:
            return f"Cannot open log for {self._spec.cshort_spec}"

    def succeed(self, externals):
        """Test reports skip externals by default."""
        if self._spec.external and not externals:
            return self.skip(msg="Skipping test of external package")

        super().succeed()
