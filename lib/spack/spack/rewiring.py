# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import shutil
import tempfile
from collections import OrderedDict

import spack.binary_distribution as bindist
import spack.error
import spack.hooks
import spack.paths
import spack.relocate as relocate
import spack.stage
import spack.store


def _relocate_spliced_links(links, orig_prefix, new_prefix):
    """Re-linking function which differs from `relocate.relocate_links` by
    reading the old link rather than the new link, since the latter wasn't moved
    in our case. This still needs to be called after the copy to destination
    because it expects the new directory structure to be in place."""
    for link in links:
        link_target = os.readlink(os.path.join(orig_prefix, link))
        link_target = re.sub('^' + orig_prefix, new_prefix, link_target)
        new_link_path = os.path.join(new_prefix, link)
        os.unlink(new_link_path)
        os.symlink(link_target, new_link_path)


def rewire(spliced_spec):
    """Given a spliced spec, this function conducts all the rewiring on all
    nodes in the DAG of that spec."""
    assert spliced_spec.spliced
    for spec in spliced_spec.traverse(order='post', root=True):
        if not spec.build_spec.package.installed:
            # TODO: May want to change this at least for the root spec...
            # spec.build_spec.package.do_install(force=True)
            raise PackageNotInstalledError(spliced_spec,
                                           spec.build_spec,
                                           spec)
        if spec.build_spec is not spec and not spec.package.installed:
            explicit = spec is spliced_spec
            rewire_node(spec, explicit)


def rewire_node(spec, explicit):
    """This function rewires a single node, worrying only about references to
    its subgraph. Binaries, text, and links are all changed in accordance with
    the splice. The resulting package is then 'installed.'"""
    tempdir = tempfile.mkdtemp()
    # copy anything installed to a temporary directory
    shutil.copytree(spec.build_spec.prefix,
                    os.path.join(tempdir, spec.dag_hash()))

    spack.hooks.pre_install(spec)
    # compute prefix-to-prefix for every node from the build spec to the spliced
    # spec
    prefix_to_prefix = OrderedDict({spec.build_spec.prefix: spec.prefix})
    for build_dep in spec.build_spec.traverse(root=False):
        prefix_to_prefix[build_dep.prefix] = spec[build_dep.name].prefix

    manifest = bindist.get_buildfile_manifest(spec.build_spec)
    platform = spack.platforms.by_name(spec.platform)

    text_to_relocate = [os.path.join(tempdir, spec.dag_hash(), rel_path)
                        for rel_path in manifest.get('text_to_relocate', [])]
    if text_to_relocate:
        relocate.relocate_text(files=text_to_relocate,
                               prefixes=prefix_to_prefix)

    bins_to_relocate = [os.path.join(tempdir, spec.dag_hash(), rel_path)
                        for rel_path in manifest.get('binary_to_relocate', [])]
    if bins_to_relocate:
        if 'macho' in platform.binary_formats:
            relocate.relocate_macho_binaries(bins_to_relocate,
                                             str(spack.store.layout.root),
                                             str(spack.store.layout.root),
                                             prefix_to_prefix,
                                             False,
                                             spec.build_spec.prefix,
                                             spec.prefix)
        if 'elf' in platform.binary_formats:
            relocate.relocate_elf_binaries(bins_to_relocate,
                                           str(spack.store.layout.root),
                                           str(spack.store.layout.root),
                                           prefix_to_prefix,
                                           False,
                                           spec.build_spec.prefix,
                                           spec.prefix)
        relocate.relocate_text_bin(binaries=bins_to_relocate,
                                   prefixes=prefix_to_prefix)
    # copy package into place (shutil.copytree)
    shutil.copytree(os.path.join(tempdir, spec.dag_hash()), spec.prefix,
                    ignore=shutil.ignore_patterns('spec.json',
                                                  'install_manifest.json'))
    if manifest.get('link_to_relocate'):
        _relocate_spliced_links(manifest.get('link_to_relocate'),
                                spec.build_spec.prefix,
                                spec.prefix)
    shutil.rmtree(tempdir)
    # handle all metadata changes; don't copy over spec.json file in .spack/
    spack.store.layout.write_spec(spec, spack.store.layout.spec_file_path(spec))
    # add to database, not sure about explicit
    spack.store.db.add(spec, spack.store.layout, explicit=explicit)

    # run post install hooks
    spack.hooks.post_install(spec)


class RewireError(spack.error.SpackError):
    """Raised when something goes wrong with rewiring."""
    def __init__(self, message, long_msg=None):
        super(RewireError, self).__init__(message, long_msg)


class PackageNotInstalledError(RewireError):
    """Raised when the build_spec for a splice was not installed."""
    def __init__(self, spliced_spec, build_spec, dep):
        super(PackageNotInstalledError, self).__init__(
            """Rewire of {0}
            failed due to missing install of build spec {1}
            for spec {2}""".format(spliced_spec, build_spec, dep))
