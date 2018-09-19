##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
