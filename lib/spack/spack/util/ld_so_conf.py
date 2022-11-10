# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import re

from llnl.util.lang import dedupe


def parse_ld_so_conf(conf_file="/etc/ld.so.conf"):
    """Parse glibc style ld.so.conf file, which specifies default search paths for the
    dynamic linker. This can in principle also be used for musl libc.

    Arguments:
        conf_file (str or bytes): Path to config file

    Returns:
        list: List of absolute search paths
    """
    # Parse in binary mode since it's faster
    is_bytes = isinstance(conf_file, bytes)
    if not is_bytes:
        conf_file = conf_file.encode("utf-8")

    # For globbing in Python2 we need to chdir.
    cwd = os.getcwd()
    try:
        paths = _process_ld_so_conf_queue([conf_file])
    finally:
        os.chdir(cwd)

    return list(paths) if is_bytes else [p.decode("utf-8") for p in paths]


def _process_ld_so_conf_queue(queue):
    include_regex = re.compile(b"include\\s")
    paths = []
    while queue:
        p = queue.pop(0)

        try:
            with open(p, "rb") as f:
                lines = f.readlines()
        except (IOError, OSError):
            continue

        for line in lines:
            # Strip comments
            comment = line.find(b"#")
            if comment != -1:
                line = line[:comment]

            # Skip empty lines
            line = line.strip()
            if not line:
                continue

            is_include = include_regex.match(line) is not None

            # If not an include, it's a literal path (no globbing here).
            if not is_include:
                # We only allow absolute search paths.
                if os.path.isabs(line):
                    paths.append(line)
                continue

            # Finally handle includes.
            include_path = line[8:].strip()
            if not include_path:
                continue

            cwd = os.path.dirname(p)
            os.chdir(cwd)
            queue.extend(os.path.join(cwd, p) for p in glob.glob(include_path))

    return dedupe(paths)
