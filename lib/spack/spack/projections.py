# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

def get_projection(projections, spec):
    """
    Get the projection for a spec from a projections dict.
    """
    all_projection = None
    for spec_like, projection in projections.items():
        if spec.satisfies(spec_like, strict=True):
            return projection
        elif spec_like == 'all':
            all_projection = projection
    return all_projection
