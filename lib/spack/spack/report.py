# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tools to produce reports of spec installations"""
import collections
import contextlib
import functools
import os
import time
import traceback
from typing import Any, Callable, Dict, List, Type

import llnl.util.lang

import spack.build_environment
import spack.fetch_strategy
import spack.install_test
import spack.package_base
import spack.reporters


def fetch_log(pkg, do_fn, dir):
    log_files = {
        "_install_task": pkg.build_log_path,
        "do_test": os.path.join(dir, spack.install_test.TestSuite.test_log_name(pkg.spec)),
    }
    try:
        with open(log_files[do_fn.__name__], "r", encoding="utf-8") as f:
            return "".join(f.readlines())
    except Exception:
        return "Cannot open log for {0}".format(pkg.spec.cshort_spec)


class InfoCollector:
    """Decorates PackageInstaller._install_task, which is called via
    PackageBase.do_install for individual specs, to collect information
    on the installation of certain specs.

    When exiting the context this change will be rolled-back.

    The data collected is available through the ``specs``
    attribute once exited, and it's organized as a list where
    each item represents the installation of one of the spec.

    """

    wrap_class: Type
    do_fn: str
    _backup_do_fn: Callable
    input_specs: List["spack.spec.Spec"]
    specs: List[Dict[str, Any]]
    dir: str

    def __init__(self, wrap_class: Type, do_fn: str, specs: List["spack.spec.Spec"], dir: str):
        #: Class for which to wrap a function
        self.wrap_class = wrap_class
        #: Action to be reported on
        self.do_fn = do_fn
        #: Backup of the wrapped class function
        self._backup_do_fn = getattr(self.wrap_class, do_fn)
        #: Specs that will be acted on
        self.input_specs = specs
        #: This is where we record the data that will be included
        #: in our report.
        self.specs = []
        #: Record directory for test log paths
        self.dir = dir

    def __enter__(self):
        # Initialize the spec report with the data that is available upfront.
        for input_spec in self.input_specs:
            name_fmt = "{0}_{1}"
            name = name_fmt.format(input_spec.name, input_spec.dag_hash(length=7))

            spec = {
                "name": name,
                "nerrors": None,
                "nfailures": None,
                "npackages": None,
                "time": None,
                "timestamp": time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()),
                "properties": [],
                "packages": [],
            }

            self.specs.append(spec)

            Property = collections.namedtuple("Property", ["name", "value"])
            spec["properties"].append(Property("architecture", input_spec.architecture))
            spec["properties"].append(Property("compiler", input_spec.compiler))

            # Check which specs are already installed and mark them as skipped
            # only for install_task
            if self.do_fn == "_install_task":
                for dep in filter(lambda x: x.installed, input_spec.traverse()):
                    package = {
                        "name": dep.name,
                        "id": dep.dag_hash(),
                        "elapsed_time": "0.0",
                        "result": "skipped",
                        "message": "Spec already installed",
                    }
                    spec["packages"].append(package)

        def gather_info(do_fn):
            """Decorates do_fn to gather useful information for
            a CI report.

            It's defined here to capture the environment and build
            this context as the installations proceed.
            """

            @functools.wraps(do_fn)
            def wrapper(instance, *args, **kwargs):
                if isinstance(instance, spack.package_base.PackageBase):
                    pkg = instance
                elif hasattr(args[0], "pkg"):
                    pkg = args[0].pkg
                else:
                    raise Exception

                # We accounted before for what is already installed
                installed_already = pkg.spec.installed

                package = {
                    "name": pkg.name,
                    "id": pkg.spec.dag_hash(),
                    "elapsed_time": None,
                    "result": None,
                    "message": None,
                    "installed_from_binary_cache": False,
                }

                # Append the package to the correct spec report. In some
                # cases it may happen that a spec that is asked to be
                # installed explicitly will also be installed as a
                # dependency of another spec. In this case append to both
                # spec reports.
                for s in llnl.util.lang.dedupe([pkg.spec.root, pkg.spec]):
                    name = name_fmt.format(s.name, s.dag_hash(length=7))
                    try:
                        item = next((x for x in self.specs if x["name"] == name))
                        item["packages"].append(package)
                    except StopIteration:
                        pass

                start_time = time.time()
                value = None
                try:
                    value = do_fn(instance, *args, **kwargs)

                    externals = kwargs.get("externals", False)
                    skip_externals = pkg.spec.external and not externals
                    if do_fn.__name__ == "do_test" and skip_externals:
                        package["result"] = "skipped"
                    else:
                        package["result"] = "success"
                    package["stdout"] = fetch_log(pkg, do_fn, self.dir)
                    package["installed_from_binary_cache"] = pkg.installed_from_binary_cache
                    if do_fn.__name__ == "_install_task" and installed_already:
                        return

                except spack.build_environment.InstallError as e:
                    # An InstallError is considered a failure (the recipe
                    # didn't work correctly)
                    package["result"] = "failure"
                    package["message"] = e.message or "Installation failure"
                    package["stdout"] = fetch_log(pkg, do_fn, self.dir)
                    package["stdout"] += package["message"]
                    package["exception"] = e.traceback
                    raise

                except (Exception, BaseException) as e:
                    # Everything else is an error (the installation
                    # failed outside of the child process)
                    package["result"] = "error"
                    package["stdout"] = fetch_log(pkg, do_fn, self.dir)
                    package["message"] = str(e) or "Unknown error"
                    package["exception"] = traceback.format_exc()
                    raise

                finally:
                    package["elapsed_time"] = time.time() - start_time

                return value

            return wrapper

        setattr(self.wrap_class, self.do_fn, gather_info(getattr(self.wrap_class, self.do_fn)))

    def __exit__(self, exc_type, exc_val, exc_tb):

        # Restore the original method in PackageBase
        setattr(self.wrap_class, self.do_fn, self._backup_do_fn)

        for spec in self.specs:
            spec["npackages"] = len(spec["packages"])
            spec["nfailures"] = len([x for x in spec["packages"] if x["result"] == "failure"])
            spec["nerrors"] = len([x for x in spec["packages"] if x["result"] == "error"])
            spec["time"] = sum([float(x["elapsed_time"]) for x in spec["packages"]])


@contextlib.contextmanager
def build_context_manager(
    reporter: spack.reporters.Reporter,
    filename: str,
    specs: List[spack.spec.Spec],
    raw_logs_dir: str,
):
    """Decorate ``PackageInstaller._install_task`` so that an installation report is emitted in
    the end.

    Args:
        reporter (spack.reporters.Reporter): object that generates the report
        filename (str):  filename for the report
        specs (list of spack.spec.Spec): specs that need reporting
        raw_logs_dir (str): TODO
    """
    collector = InfoCollector(
        spack.package_base.PackageInstaller, "_install_task", specs, raw_logs_dir
    )
    try:
        with collector:
            yield
    finally:
        reporter.build_report(filename, specs=collector.specs)


@contextlib.contextmanager
def test_context_manager(
    reporter: spack.reporters.Reporter,
    filename: str,
    specs: List[spack.spec.Spec],
    raw_logs_dir: str,
):
    """Decorate ``PackageBase.do_test`` so that a test report is emitted in the end.

    Args:
        reporter (spack.reporters.Reporter): object that generates the report
        filename (str):  filename for the report
        specs (list of spack.spec.Spec): specs that need reporting
        raw_logs_dir (str): TODO
    """
    collector = InfoCollector(spack.package_base.PackageBase, "do_test", specs, raw_logs_dir)
    try:
        with collector:
            yield
    finally:
        reporter.test_report(filename, specs=collector.specs)
