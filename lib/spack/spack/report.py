# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tools to produce reports of spec installations"""
import codecs
import collections
import functools
import os
import time
import traceback

import llnl.util.lang

import spack.build_environment
import spack.fetch_strategy
import spack.package_base
from spack.install_test import TestSuite
from spack.reporter import Reporter
from spack.reporters.cdash import CDash
from spack.reporters.junit import JUnit
from spack.spec import Spec

report_writers = {None: Reporter, "junit": JUnit, "cdash": CDash}

#: Allowed report formats
valid_formats = list(report_writers.keys())

__all__ = ["valid_formats", "collect_info"]


def fetch_log(pkg, do_fn, dir):
    log_files = {
        "_install_task": pkg.build_log_path,
        "do_test": os.path.join(dir, TestSuite.test_log_name(pkg.spec)),
    }
    try:
        with codecs.open(log_files[do_fn.__name__], "r", "utf-8") as f:
            return "".join(f.readlines())
    except Exception:
        return "Cannot open log for {0}".format(pkg.spec.cshort_spec)


def spec_name(spec):
    return "{0}_{1}".format(spec.name, spec.dag_hash(length=7))


class SpecData(dict):
    def __init__(self, spec):
        kv = [
            ("name", spec_name(spec)),
            ("nerrors", None),
            ("nfailures", None),
            ("npackages", None),
            ("time", None),
            ("timestamp", time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())),
            ("properties", []),
            ("packages", []),
        ]
        dict.__init__(self, kv)

        Property = collections.namedtuple("Property", ["name", "value"])
        self["properties"].append(Property("architecture", spec.architecture))
        self["properties"].append(Property("compiler", spec.compiler))

    def add_package(self, spec_or_pkg, **kwargs):
        spec = spec_or_pkg if isinstance(spec_or_pkg, Spec) else None
        if spec:
            package = {
                "name": spec.name,
                "id": spec.dag_hash(),
                "elapsed_time": kwargs.get("elapsed_time"),
                "result": kwargs.get("result"),
                "message": kwargs.get("message"),
                "installed_from_binary_cache": kwargs.get("installed_from_binary_cache", False),
            }
        else:
            package = kwargs.get("package")

        if package:
            self["packages"].append(package)

        return package

    def add_skipped_package(self, spec, message):
        self.add_package(
            spec,
            elapsed_time="0.0",
            result="skipped",
            message=message,
        )

    def summarize(self):
        self["npackages"] = len(self["packages"])
        self["nfailures"] = len([x for x in self["packages"] if x["result"] == "failure"])
        self["nerrors"] = len([x for x in self["packages"] if x["result"] == "error"])
        self["time"] = sum([float(x["elapsed_time"]) for x in self["packages"]])


class InfoCollector(object):
    """Decorates PackageInstaller._install_task, which is called via
    PackageBase.do_install for individual specs, to collect information
    on the installation of certain specs.

    When exiting the context this change will be rolled-back.

    The data collected is available through the ``specs``
    attribute once exited, and it's organized as a list where
    each item represents the installation of one of the spec.

    Args:
        specs (list of Spec): specs whose install information will
           be recorded
    """

    def __init__(self, wrap_class, do_fn, specs, dir):
        #: Class for which to wrap a function
        self.wrap_class = wrap_class
        #: Action to be reported on
        self.do_fn = do_fn
        #: Backup of PackageBase function
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
            spec_data = SpecData(input_spec)
            self.specs.append(spec_data)

            # Check which specs are already installed and mark them as skipped
            # only for install_task
            if self.do_fn == "_install_task":
                for dep in filter(lambda x: x.installed, input_spec.traverse()):
                    spec_data.add_skipped_package(dep, "Spec already installed")

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

                # Append the package to the correct spec report. In some
                # cases it may happen that a spec that is asked to be
                # installed explicitly will also be installed as a
                # dependency of another spec. In this case append to both
                # spec reports.
                package = None
                for s in llnl.util.lang.dedupe([pkg.spec.root, pkg.spec]):
                    name = spec_name(s)
                    try:
                        spec_data = next((x for x in self.specs if x["name"] == name))
                        package = spec_data.add_package(package or pkg.spec)
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

        for spec_data in self.specs:
            spec_data.summarize()


class collect_info(object):
    """Collects information to build a report while installing
    and dumps it on exit.

    If the format name is not ``None``, this context manager decorates
    PackageInstaller._install_task when entering the context for a
    PackageBase.do_install operation and unrolls the change when exiting.

    Within the context, only the specs that are passed to it
    on initialization will be recorded for the report. Data from
    other specs will be discarded.

    Examples:

        .. code-block:: python

            # The file 'junit.xml' is written when exiting
            # the context
            s = [Spec('hdf5').concretized()]
            with collect_info(PackageBase, do_install, s, 'junit', 'a.xml'):
                # A report will be generated for these specs...
                for spec in s:
                    getattr(class, function)(spec)
                # ...but not for this one
                Spec('zlib').concretized().do_install()

    Args:
        class: class on which to wrap a function
        function: function to wrap
        format_name (str or None): one of the supported formats
        args (dict): args passed to function

    Raises:
        ValueError: when ``format_name`` is not in ``valid_formats``
    """

    def __init__(self, cls, function, format_name, args):
        self.cls = cls
        self.function = function
        self.filename = None
        self.ctest_parsing = getattr(args, "ctest_parsing", False)
        if args.cdash_upload_url:
            self.format_name = "cdash"
            self.filename = "cdash_report"
        else:
            self.format_name = format_name
        # Check that the format is valid.
        if self.format_name not in valid_formats:
            raise ValueError("invalid report type: {0}".format(self.format_name))
        self.report_writer = report_writers[self.format_name](args)

    def __call__(self, type, dir=None):
        self.type = type
        self.dir = dir or os.getcwd()
        return self

    def concretization_report(self, msg):
        self.report_writer.concretization_report(self.filename, msg)

    def __enter__(self):
        if self.format_name:
            # Start the collector and patch self.function on appropriate class
            self.collector = InfoCollector(self.cls, self.function, self.specs, self.dir)
            self.collector.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.format_name:
            # Close the collector and restore the original function
            self.collector.__exit__(exc_type, exc_val, exc_tb)

            report_data = {"specs": self.collector.specs}
            report_data["ctest-parsing"] = self.ctest_parsing
            report_fn = getattr(self.report_writer, "%s_report" % self.type)
            report_fn(self.filename, report_data)
