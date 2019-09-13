# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import json
import hashlib
import base64
import sys

import spack.store
import spack.util.file_permissions as fp
import spack.verify

def create_manifest_entry(path):
    data = {}
    stat = os.stat(path)

    data['mode'] = stat.st_mode
    data['owner'] = stat.st_uid
    data['group'] = stat.st_gid

    if os.path.islink(path):
        data['type'] = 'link'
        data['dest'] = os.readlink(path)

    elif os.path.isdir(path):
        data['type'] = 'dir'

    else:
        data['type'] = 'file'
        data['hash'] = spack.verify.compute_hash(path)
        data['time'] = stat.st_mtime
        data['size'] = stat.st_size

    return data


def generate_manifest(prefix):
    manifest = {}
    for root, dirs, files in os.walk(prefix):
        for entry in list(dirs + files):
            path = os.path.join(root, entry)
            manifest[path] = create_manifest_entry(path)
    manifest[prefix] = create_manifest_entry(prefix)

    return manifest

def post_install(spec):
    if not spec.external:
        manifest_file = os.path.join(spec.prefix,
                                     spack.store.layout.metadata_dir,
                                     spack.store.layout.manifest_file_name)

        if not manifest_file:
            tty.debug("Writing manifest file: No manifest from binary")

            manifest = generate_manifest(spec.prefix)

            with open(manifest_file, 'wb') as f:
                js = json.dumps(manifest, f)
                if sys.version_info[0] >= 3:
                    js = js.encode()
                f.write(js)

            fp.set_permissions_by_spec(manifest_file, spec)
