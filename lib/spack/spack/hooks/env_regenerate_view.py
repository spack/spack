# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

def post_env_install(env, new_installs):
    """
    Update the view of an environment after installation.

    Parameters:
        env (spack.environment.Environment): the environment
        new_installs (list): list of newly installed specs
    """
    with env.write_transaction():
        env.regenerate_views()
