# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class ImpossibleConcretization(Package):
    """Package that should be impossible to concretize due to a conflict
    with target ranges. See Issue 19981.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/example-1.0.tar.gz"

    version(1.0, '0123456789abcdef0123456789abcdef')

    conflicts('target=x86_64:')
