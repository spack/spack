# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.compilers.xl


class XlR(spack.compilers.xl.Xl):
    # Named wrapper links within build_env_path
    link_paths = {'cc': 'xl_r/xlc_r',
                  'cxx': 'xl_r/xlc++_r',
                  'f77': 'xl_r/xlf_r',
                  'fc': 'xl_r/xlf90_r'}
