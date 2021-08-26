# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from llnl.util import tty


def post_env_install(env, new_installs):
    """
    Install log links for all newly installed specs in an environment

    Parameters:
        env (spack.environment.Environment): the environment
        new_installs (list): list of newly installed specs
    """
    for spec in new_installs:
        try:
            env._install_log_links(spec)
        except OSError as e:
            tty.warn('Could not install log links for {0}: {1}'
                     .format(spec.name, str(e)))
