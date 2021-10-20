# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import tempfile
from pprint import pprint

from ordereddict_backport import OrderedDict

import spack.binary_distribution as bindist
import spack.hooks
import spack.paths
import spack.relocate as relocate
import spack.stage
import spack.store
from spack.installer import PackageInstaller
from spack.spec import Spec


def rewire(spliced_spec):
    """Will be the main, externally-facing function that simply takes a spliced
    spec and does all rewiring."""
    assert spliced_spec.spliced
    for spec in spliced_spec.traverse(order='post', root=True):
        if not spec.build_spec.package.installed:
            raise RuntimeError('Pure spec package was not installed')
        if spec.build_spec is not spec:
            explicit = spec is spliced_spec
            rewire_node(spec, explicit)


def rewire_node(spec, explicit):
    """Will be the mostly-internal function that gets called iteratively."""
    tempdir = tempfile.mkdtemp()
    # copy anything installed to a temporary directory
    shutil.copytree(spec.build_spec.prefix,
                    os.path.join(tempdir, spec.dag_hash()))

    # compute prefix-to-prefix for every node from the build spec to the spliced
    # spec
    prefix_to_prefix = OrderedDict({spec.build_spec.prefix: spec.prefix})
    for build_dep in spec.build_spec.traverse(root=False):
        prefix_to_prefix[build_dep.prefix] = spec[build_dep.name].prefix
    # determine files that need to be relocated as in write_buildinfo_file
    manifest = bindist.get_buildfile_manifest(spec.build_spec)
    pprint(manifest)
    # determine elf or macho
    platform = spack.platforms.by_name(spec.platform)
    if manifest.get('relocate_binaries'):
        binaries_to_relocate = [os.path.join(tempdir, spec.dag_hash(), filename)
                                for filename in manifest.get('relocate_binaries')
                                ]
    if manifest.get('text_to_relocate'):
        text_to_relocate = [os.path.join(tempdir, spec.dag_hash(), filename)
                            for filename in manifest.get('text_to_relocate')]
    if manifest.get('link_to_relocate'):
        link_to_relocate = [os.path.join(tempdir, spec.dag_hash(), filename)
                            for filename in manifest.get('link_to_relocate')]
    if 'macho' in platform.binary_formats and manifest.get('relocate_binaries'):
        relocate.relocate_macho_binaries(binaries_to_relocate,
                                         str(spack.store.layout.root),
                                         str(spack.store.layout.root),
                                         prefix_to_prefix,
                                         False,
                                         spec.build_spec.prefix,
                                         spec.prefix
                                         )
    if ('elf' in platform.binary_formats and
        manifest.get('relocate_binaries') and
        manifest.get('link_to_relocate')):
        relocate.relocate_elf_binaries(binaries_to_relocate,
                                       str(spack.store.layout.root),
                                       str(spack.store.layout.root),
                                       prefix_to_prefix,
                                       False,
                                       spec.build_spec.prefix,
                                       spec.prefix
                                       )
        relocate.relocate_links(link_to_relocate,
                                str(spack.store.layout.root),
                                spec.build_spec.prefix,
                                spec.prefix)
    if manifest.get('text_to_relocate'):
        relocate.relocate_text(files=text_to_relocate,
                               prefixes=prefix_to_prefix)
    # copy package into place (shutil.copytree)
    shutil.copytree(os.path.join(tempdir, spec.dag_hash()), spec.prefix,
                    ignore=shutil.ignore_patterns('.spack/spec.json'))
    # handle all metadata changes; don't copy over spec.json file in .spack/
    spack.store.layout.write_spec(spec, spack.store.layout.spec_file_path(spec))
    # add to database, not sure about explicit
    spack.store.db.add(spec, spack.store.layout, explicit=explicit)
    spack.store.db.add(spec, spack.store.layout, explicit=explicit)

    # run post install hooks
    spack.hooks.post_install(spec)
