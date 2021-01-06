# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.container
import spack.schema.container


def test_images_in_schema():
    properties = spack.schema.container.container_schema['properties']
    allowed_images = set(
        properties['images']['anyOf'][0]['properties']['os']['enum']
    )
    images_in_json = set(x for x in spack.container.images.data()['images'])
    assert images_in_json == allowed_images
