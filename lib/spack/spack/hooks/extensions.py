# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack
from spack.filesystem_view import YamlFilesystemView


def pre_uninstall(spec):
    pkg = spec.package
    assert spec.concrete

    if pkg.is_extension:
        target = pkg.extendee_spec.prefix
        view = YamlFilesystemView(target, spack.store.layout)

        if pkg.is_activated(view):
            # deactivate globally
            pkg.do_deactivate(force=True)
