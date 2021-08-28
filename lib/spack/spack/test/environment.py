# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pickle

from spack.environment import Environment


def test_environment_pickle(tmpdir):
    env1 = Environment(str(tmpdir))
    obj = pickle.dumps(env1)
    env2 = pickle.loads(obj)
    assert isinstance(env2, Environment)
