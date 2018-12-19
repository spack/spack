# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.spec import Spec


def test_global_activation(install_mockery, mock_fetch):
    """This test ensures that views which are maintained inside of an extendee
       package's prefix are maintained as expected and are compatible with
       global activations prior to #7152.
    """
    spec = Spec('extension1').concretized()
    pkg = spec.package
    pkg.do_install()
    pkg.do_activate()

    extendee_spec = spec['extendee']
    extendee_pkg = spec['extendee'].package
    view = extendee_pkg.view()
    assert pkg.is_activated(view)

    expected_path = os.path.join(
        extendee_spec.prefix, '.spack', 'extensions.yaml')
    assert (view.extensions_layout.extension_file_path(extendee_spec) ==
            expected_path)
