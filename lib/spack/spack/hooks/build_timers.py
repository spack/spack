# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

def post_install(spec, timer=None):
    if not timer:
        return
    with open(spec.package.times_log_path, 'w') as timelog:
        timer.write_json(timelog)
