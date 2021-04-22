# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.lang


class ConcreteSpecRegistry(object):
    """
    The ConcreteSpecRegistry is just a dictionary containing all known
    concrete specs ever seen by spack, keyed by dag hash.
    """
    def __init__(self):
        self._registry = {}

    def populate(self):
        import spack.binary_distribution as bindist
        import spack.environment as ev
        import spack.store

        for key, spec in spack.store.db.all_specs():
            self._registry[key] = spec

        bindist.binary_index.update()
        for spec in bindist.binary_index.get_all_built_specs():
            self._registry[spec.dag_hash()] = spec

        active_env = ev.get_env(None, None)
        if active_env:
            for s in active_env.all_specs():
                self._registry[s.dag_hash()] = s

    def get_by_hash(self, dag_hash):
        if not self._registry:
            self.populate()

        matches = [spec for h, spec in self._registry.items()
                   if h.startswith(dag_hash)]

        return matches


def _specs():
    return ConcreteSpecRegistry()


specs = llnl.util.lang.Singleton(_specs)
