# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys
from subprocess import PIPE, run
from typing import Optional

import spack.spec
import spack.util.elf


def _libc_from_ldd(ldd: str) -> Optional["spack.spec.Spec"]:
    try:
        result = run([ldd, "--version"], stdout=PIPE, stderr=PIPE, check=False)
        stdout = result.stdout.decode("utf-8")
    except Exception:
        return None

    if not re.search("gnu|glibc", stdout, re.IGNORECASE):
        return None

    version_str = re.match(r".+\(.+\) (.+)", stdout)
    if not version_str:
        return None
    try:
        return spack.spec.Spec(f"glibc@={version_str.group(1)}")
    except Exception:
        return None


def libc_from_dynamic_linker(dynamic_linker: str) -> Optional["spack.spec.Spec"]:
    if not os.path.exists(dynamic_linker):
        return None

    # The dynamic linker is usually installed in the same /lib(64)?/ld-*.so path across all
    # distros. The rest of libc is elsewhere, e.g. /usr. Typically the dynamic linker is then
    # a symlink into /usr/lib, which we use to for determining the actual install prefix of
    # libc.
    realpath = os.path.realpath(dynamic_linker)

    prefix = os.path.dirname(realpath)
    # Remove the multiarch suffix if it exists
    if os.path.basename(prefix) not in ("lib", "lib64"):
        prefix = os.path.dirname(prefix)

    # Non-standard install layout -- just bail.
    if os.path.basename(prefix) not in ("lib", "lib64"):
        return None

    prefix = os.path.dirname(prefix)

    # Now try to figure out if glibc or musl, which is the only ones we support.
    # In recent glibc we can simply execute the dynamic loader. In musl that's always the case.
    try:
        result = run([dynamic_linker, "--version"], stdout=PIPE, stderr=PIPE, check=False)
        stdout = result.stdout.decode("utf-8")
        stderr = result.stderr.decode("utf-8")
    except Exception:
        return None

    # musl prints to stderr
    if stderr.startswith("musl libc"):
        version_str = re.search(r"^Version (.+)$", stderr, re.MULTILINE)
        if not version_str:
            return None
        try:
            spec = spack.spec.Spec(f"musl@={version_str.group(1)}")
            spec.external_path = prefix
            return spec
        except Exception:
            return None
    elif re.search("gnu|glibc", stdout, re.IGNORECASE):
        # output is like "ld.so (...) stable release version 2.33." write a regex for it
        match = re.search(r"version (\d+\.\d+(?:\.\d+)?)", stdout)
        if not match:
            return None
        try:
            version = match.group(1)
            spec = spack.spec.Spec(f"glibc@={version}")
            spec.external_path = prefix
            return spec
        except Exception:
            return None
    else:
        # Could not get the version by running the dynamic linker directly. Instead locate `ldd`
        # relative to the dynamic linker.
        ldd = os.path.join(prefix, "bin", "ldd")
        if not os.path.exists(ldd):
            # If `/lib64/ld.so` was not a symlink to `/usr/lib/ld.so` we can try to use /usr as
            # prefix. This is the case on ubuntu 18.04 where /lib != /usr/lib.
            if prefix != "/":
                return None
            prefix = "/usr"
            ldd = os.path.join(prefix, "bin", "ldd")
            if not os.path.exists(ldd):
                return None
        maybe_spec = _libc_from_ldd(ldd)
        if not maybe_spec:
            return None
        maybe_spec.external_path = prefix
        return maybe_spec


def libc_from_current_python_process() -> Optional["spack.spec.Spec"]:
    if not sys.executable:
        return None

    dynamic_linker = spack.util.elf.pt_interp(sys.executable)

    if not dynamic_linker:
        return None

    return libc_from_dynamic_linker(dynamic_linker)
