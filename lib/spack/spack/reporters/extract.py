# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re
import xml.sax.saxutils
from datetime import datetime

import llnl.util.tty as tty

# The keys here represent the only recognized (ctest/cdash) status values
completed = {"failed": "Completed", "passed": "Completed", "notrun": "No tests to run"}

log_regexp = re.compile(r"^==> \[([0-9:.\-]*)(?:, [0-9]*)?\] (.*)")
returns_regexp = re.compile(r"\[([0-9 ,]*)\]")

skip_msgs = ["Testing package", "Results for", "Detected the following"]
skip_regexps = [re.compile(r"{0}".format(msg)) for msg in skip_msgs]

status_values = ["FAILED", "PASSED", "NO-TESTS"]
status_regexps = [re.compile(r"^({0})".format(stat)) for stat in status_values]


def add_part_output(part, line):
    if part:
        part["loglines"].append(xml.sax.saxutils.escape(line))


def elapsed(current, previous):
    if not (current and previous):
        return 0

    diff = current - previous
    tty.debug("elapsed = %s - %s = %s" % (current, previous, diff))
    return diff.total_seconds()


def expected_failure(line):
    if not line:
        return False

    match = returns_regexp.search(line)
    xfail = "0" not in match.group(0) if match else False
    return xfail


def new_part():
    return {
        "command": None,
        "completed": "Unknown",
        "desc": None,
        "elapsed": None,
        "name": None,
        "loglines": [],
        "output": None,
        "status": "passed",
    }


def part_name(source):
    # TODO: Should be passed the package prefix and only remove it
    elements = []
    for e in source.replace("'", "").split(" "):
        elements.append(os.path.basename(e) if os.sep in e else e)
    return "_".join(elements)


def process_part_end(part, curr_time, last_time):
    if part:
        if not part["elapsed"]:
            part["elapsed"] = elapsed(curr_time, last_time)

        stat = part["status"]
        if stat in completed:
            if stat == "passed" and expected_failure(part["desc"]):
                part["completed"] = "Expected to fail"
            elif part["completed"] == "Unknown":
                part["completed"] = completed[stat]
        part["output"] = "\n".join(part["loglines"])


def timestamp(time_string):
    return datetime.strptime(time_string, "%Y-%m-%d-%H:%M:%S.%f")


def skip(line):
    for regex in skip_regexps:
        match = regex.search(line)
        if match:
            return match


def status(line):
    for regex in status_regexps:
        match = regex.search(line)
        if match:
            stat = match.group(0)
            stat = "notrun" if stat == "NO-TESTS" else stat
            return stat.lower()


def extract_test_parts(default_name, outputs):
    parts = []
    part = {}
    testdesc = ""
    last_time = None
    curr_time = None
    for line in outputs:
        line = line.strip()
        if not line:
            add_part_output(part, line)
            continue

        if skip(line):
            continue

        # Skipped tests start with "Skipped" and end with "package"
        if line.startswith("Skipped") and line.endswith("package"):
            part = new_part()
            part["command"] = "Not Applicable"
            part["completed"] = line
            part["elapsed"] = 0.0
            part["name"] = default_name
            part["status"] = "notrun"
            parts.append(part)
            continue

        # Process Spack log messages
        if line.find("==>") != -1:
            match = log_regexp.search(line)
            if match:
                curr_time = timestamp(match.group(1))
                msg = match.group(2)

                # Skip logged message for caching build-time data
                if msg.startswith("Installing"):
                    continue

                # New command means the start of a new test part
                if msg.startswith("'") and msg.endswith("'"):
                    # Update the last part processed
                    process_part_end(part, curr_time, last_time)

                    part = new_part()
                    part["command"] = msg
                    part["name"] = part_name(msg)
                    parts.append(part)

                    # Save off the optional test description if it was
                    # tty.debuged *prior to* the command and reset
                    if testdesc:
                        part["desc"] = testdesc
                        testdesc = ""

                else:
                    # Update the last part processed since a new log message
                    # means a non-test action
                    process_part_end(part, curr_time, last_time)

                    if testdesc:
                        # We had a test description but no command so treat
                        # as a new part (e.g., some import tests)
                        part = new_part()
                        part["name"] = "_".join(testdesc.split())
                        part["command"] = "unknown"
                        part["desc"] = testdesc
                        parts.append(part)
                        process_part_end(part, curr_time, curr_time)

                    # Assuming this is a description for the next test part
                    testdesc = msg

            else:
                tty.debug("Did not recognize test output '{0}'".format(line))

            # Each log message potentially represents a new test part so
            # save off the last timestamp
            last_time = curr_time
            continue

        # Check for status values
        stat = status(line)
        if stat:
            if part:
                part["status"] = stat
                add_part_output(part, line)
            else:
                tty.warn("No part to add status from '{0}'".format(line))
            continue

        add_part_output(part, line)

    # Process the last lingering part IF it didn't generate status
    process_part_end(part, curr_time, last_time)

    # If no parts, create a skeleton to flag that the tests are not run
    if not parts:
        part = new_part()
        stat = "notrun"
        part["command"] = "Not Applicable"
        part["completed"] = completed[stat]
        part["elapsed"] = 0.0
        part["name"] = default_name
        part["status"] = stat
        parts.append(part)

    return parts
