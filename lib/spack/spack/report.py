# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Hooks to produce reports of spec installations"""
import collections
import gzip
import os
import time
import traceback

import llnl.util.filesystem as fs

import spack.build_environment
import spack.util.spack_json as sjson

reporter = None
report_file = None

Property = collections.namedtuple("Property", ["name", "value"])


class Record(dict):
    def __getattr__(self, name):
        # only called if no attribute exists
        if name in self:
            return self[name]
        raise AttributeError(f"RequestRecord for {self.name} has no attribute {name}")

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self[name] = value


class RequestRecord(Record):
    def __init__(self, spec):
        super().__init__()
        self._spec = spec
        self.name = spec.name
        self.errors = None
        self.nfailures = None
        self.npackages = None
        self.time = None
        self.timestamp = time.strftime("%a, d %b %Y %H:%M:%S", time.gmtime())
        self.properties = [
            Property("architecture", spec.architecture),
            # Property("compiler", spec.compiler),
        ]
        self.packages = []

    def skip_installed(self):
        for dep in filter(lambda x: x.installed, self._spec.traverse()):
            record = InstallRecord(dep)
            record.skip(msg="Spec already installed")
            self.packages.append(record)

    def append_record(self, record):
        self.packages.append(record)

    def summarize(self):
        self.npackages = len(self.packages)
        self.nfailures = len([r for r in self.packages if r.result == "failure"])
        self.nerrors = len([r for r in self.packages if r.result == "error"])
        self.time = sum(float(r.elapsed_time or 0.0) for r in self.packages)


class SpecRecord(Record):
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


class InstallRecord(SpecRecord):
    def __init__(self, spec):
        super().__init__(spec)
        self.result = None
        self.message = None
        self.installed_from_binary_cache = None

    def fetch_log(self):
        try:
            if os.path.exists(self._package.install_log_path):
                stream = gzip.open(self._package.install_log_path, "rt", encoding="utf-8")
            else:
                stream = open(self._package.log_path, encoding="utf-8")
            with stream as f:
                return f.read()
        except OSError:
            return f"Cannot open log for {self._spec.cshort_spec}"

    def fetch_time(self):
        try:
            with open(self._package.times_log_path, "r", encoding="utf-8") as f:
                data = sjson.load(f.read())
            return data["total"]
        except Exception:
            return None

    def succeed(self):
        self.result = "success"
        self.stdout = self.fetch_log()
        self.installed_from_binary_cache = self._package.installed_from_binary_cache
        assert self._start_time, "Start time is None"
        self.elapsed_time = time.time() - self._start_time

    def fail(self, exc):
        if isinstance(exc, spack.build_environment.InstallError):
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
