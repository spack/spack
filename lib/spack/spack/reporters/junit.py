# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import xml.sax.saxutils
from typing import Any, Dict, List

import spack.tengine

from .base import Reporter
from .extract import extract_test_parts

#: JUnit result for each stand-alone test part status (anything else passed)
_PART_RESULTS = {"failed": "failure", "skipped": "skipped", "notrun": "skipped"}


def _package_testcase(package) -> Dict[str, Any]:
    """One test case for a whole package (installs, or tests without parts)."""
    return {
        "classname": package["name"],
        "name": package["id"],
        "time": package.get("elapsed_time"),
        "result": package.get("result"),
        "message": package.get("message"),
        "exception": package.get("exception"),
        "stdout": package.get("stdout"),
        "stderr": package.get("stderr"),
    }


def _test_part_testcases(package) -> List[Dict[str, Any]]:
    """One test case per stand-alone test part of the package, like CDash."""
    if not package.get("stdout"):
        return [_package_testcase(package)]

    cases = []
    for part in extract_test_parts(package["name"], package["stdout"].splitlines()):
        # extract_test_parts escapes the log lines for CDash; the template escapes them again
        output = xml.sax.saxutils.unescape(part["output"] or "")
        result = _PART_RESULTS.get(part["status"], "success")
        message = None
        if result == "failure":
            failed = [line for line in output.splitlines() if line.startswith("FAILED")]
            message = failed[0] if failed else "Test part failed"
        cases.append(
            {
                "classname": package["name"],
                "name": part["name"],
                "time": part["elapsed"] or 0.0,
                "result": result,
                "message": message,
                "exception": output,
                "stdout": output,
                "stderr": None,
            }
        )

    # The package failed outside of its test parts (e.g., the test process crashed),
    # so keep the package-level failure instead of reporting only passing parts.
    if package.get("result") in ("failure", "error") and not any(
        case["result"] == "failure" for case in cases
    ):
        return [_package_testcase(package)]

    return cases


def _testsuite(spec, testcases: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "name": spec.name,
        "errors": len([case for case in testcases if case["result"] == "error"]),
        "tests": len(testcases),
        "failures": len([case for case in testcases if case["result"] == "failure"]),
        "time": spec.time,
        "timestamp": spec.timestamp,
        "properties": spec.properties,
        "testcases": testcases,
    }


class JUnit(Reporter):
    """Generate reports of spec installations for JUnit."""

    _jinja_template = "reports/junit.xml"

    def concretization_report(self, filename, msg):
        pass

    def _write_report(self, filename, testsuites):
        if not (os.path.splitext(filename))[1]:
            # Ensure the report name will end with the proper extension;
            # otherwise, it currently defaults to the "directory" name.
            filename = filename + ".xml"

        report_data = {"testsuites": testsuites}

        with open(filename, "w", encoding="utf-8") as f:
            env = spack.tengine.make_environment()
            t = env.get_template(self._jinja_template)
            f.write(t.render(report_data))

    def build_report(self, filename, specs):
        testsuites = []
        for spec in specs:
            spec.summarize()
            testcases = [_package_testcase(package) for package in spec.packages]
            testsuites.append(_testsuite(spec, testcases))
        self._write_report(filename, testsuites)

    def test_report(self, filename, specs):
        testsuites = []
        for spec in specs:
            spec.summarize()
            testcases = [case for pkg in spec.packages for case in _test_part_testcases(pkg)]
            testsuites.append(_testsuite(spec, testcases))
        self._write_report(filename, testsuites)
