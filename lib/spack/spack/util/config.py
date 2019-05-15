# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Convenience utilities for common config queries.
"""
import spack.config


def has_mirrors(mirrors=None, scope=None):
    for _ in iter_mirrors(mirrors=mirrors, scope=scope):
        return True

    return False


def iter_mirrors(mirrors=None, scope=None):
    return ((name,
             getattr(mirror, 'fetch', mirror),
             getattr(mirror, 'push', mirror))

            for mirror in (
                mirrors.items() if mirrors is not None else
                spack.config.get('mirrors', scope=scope).items()))


def lookup_mirror(name, mirrors=None, scope=None):
    if mirrors is None:
        mirrors = spack.config.get('mirrors', scope=scope)

    mirror = mirrors.get(name)

    # if no mirror found, assume that [name] is a mirror url, verbatim
    return ((name, name) if mirror is None else
                (getattr(mirror, 'fetch', mirror),
                 getattr(mirror, 'push', mirror)))

