# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import base64
import hashlib
import os

import llnl.util.tty as tty

import spack.filesystem_view
import spack.store
import spack.util.file_permissions as fp
import spack.util.spack_json as sjson


def compute_hash(path):
    with open(path, "rb") as f:
        sha1 = hashlib.sha1(f.read()).digest()
        b32 = base64.b32encode(sha1)
        return b32.decode()


def create_manifest_entry(path):
    data = {}

    if os.path.exists(path):
        stat = os.stat(path)

        data["mode"] = stat.st_mode
        data["owner"] = stat.st_uid
        data["group"] = stat.st_gid

        if os.path.islink(path):
            data["type"] = "link"
            data["dest"] = os.readlink(path)

        elif os.path.isdir(path):
            data["type"] = "dir"

        else:
            data["type"] = "file"
            data["hash"] = compute_hash(path)
            data["time"] = stat.st_mtime
            data["size"] = stat.st_size

    return data


def write_manifest(spec):
    manifest_file = os.path.join(
        spec.prefix, spack.store.layout.metadata_dir, spack.store.layout.manifest_file_name
    )

    if not os.path.exists(manifest_file):
        tty.debug("Writing manifest file: No manifest from binary")

        manifest = {}
        for root, dirs, files in os.walk(spec.prefix):
            for entry in list(dirs + files):
                path = os.path.join(root, entry)
                manifest[path] = create_manifest_entry(path)
        manifest[spec.prefix] = create_manifest_entry(spec.prefix)

        with open(manifest_file, "w") as f:
            sjson.dump(manifest, f)

        fp.set_permissions_by_spec(manifest_file, spec)


def check_entry(path, data):
    res = VerificationResults()

    if not data:
        res.add_error(path, "added")
        return res

    stat = os.stat(path)

    # Check for all entries
    if stat.st_mode != data["mode"]:
        res.add_error(path, "mode")
    if stat.st_uid != data["owner"]:
        res.add_error(path, "owner")
    if stat.st_gid != data["group"]:
        res.add_error(path, "group")

    # Check for symlink targets  and listed as symlink
    if os.path.islink(path):
        if data["type"] != "link":
            res.add_error(path, "type")
        if os.readlink(path) != data.get("dest", ""):
            res.add_error(path, "link")

    # Check directories are listed as directory
    elif os.path.isdir(path):
        if data["type"] != "dir":
            res.add_error(path, "type")

    else:
        # Check file contents against hash and listed as file
        # Check mtime and size as well
        if stat.st_size != data["size"]:
            res.add_error(path, "size")
        if stat.st_mtime != data["time"]:
            res.add_error(path, "mtime")
        if data["type"] != "file":
            res.add_error(path, "type")
        if compute_hash(path) != data.get("hash", ""):
            res.add_error(path, "hash")

    return res


def check_file_manifest(filename):
    dirname = os.path.dirname(filename)

    results = VerificationResults()
    while spack.store.layout.metadata_dir not in os.listdir(dirname):
        if dirname == os.path.sep:
            results.add_error(filename, "not owned by any package")
            return results
        dirname = os.path.dirname(dirname)

    manifest_file = os.path.join(
        dirname, spack.store.layout.metadata_dir, spack.store.layout.manifest_file_name
    )

    if not os.path.exists(manifest_file):
        results.add_error(filename, "manifest missing")
        return results

    try:
        with open(manifest_file, "r") as f:
            manifest = sjson.load(f)
    except Exception:
        results.add_error(filename, "manifest corrupted")
        return results

    if filename in manifest:
        results += check_entry(filename, manifest[filename])
    else:
        results.add_error(filename, "not owned by any package")
    return results


def check_spec_manifest(spec):
    prefix = spec.prefix

    results = VerificationResults()
    manifest_file = os.path.join(
        prefix, spack.store.layout.metadata_dir, spack.store.layout.manifest_file_name
    )

    if not os.path.exists(manifest_file):
        results.add_error(prefix, "manifest missing")
        return results

    try:
        with open(manifest_file, "r") as f:
            manifest = sjson.load(f)
    except Exception:
        results.add_error(prefix, "manifest corrupted")
        return results

    for root, dirs, files in os.walk(prefix):
        for entry in list(dirs + files):
            path = os.path.join(root, entry)

            # Do not check manifest file. Can't store your own hash
            if path == manifest_file:
                continue

            data = manifest.pop(path, {})
            results += check_entry(path, data)

    results += check_entry(prefix, manifest.pop(prefix, {}))

    for path in manifest:
        results.add_error(path, "deleted")

    return results


class VerificationResults(object):
    def __init__(self):
        self.errors = {}

    def add_error(self, path, field):
        self.errors[path] = self.errors.get(path, []) + [field]

    def __add__(self, vr):
        for path, fields in vr.errors.items():
            self.errors[path] = self.errors.get(path, []) + fields
        return self

    def has_errors(self):
        return bool(self.errors)

    def json_string(self):
        return sjson.dump(self.errors)

    def __str__(self):
        res = ""
        for path, fields in self.errors.items():
            res += "%s verification failed with error(s):\n" % path
            for error in fields:
                res += "    %s\n" % error

        if not res:
            res += "No Errors"
        return res
