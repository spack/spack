# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyParmed(PythonPackage):
    """ParmEd is a package designed to facilitate creating and easily manipulating molecular 
    systems that are fully described by a common classical force field. Supported force fields 
    include Amber, CHARMM, AMOEBA, and several others that share a similar functional form 
    (e.g., GROMOS)."""

    homepage = "https://github.com/ParmEd/ParmEd"
    git      = "git@github.com:ParmEd/ParmEd.git"
    url      = "https://github.com/ParmEd/ParmEd/archive/3.2.0.tar.gz"

    version('3.2.0', sha256='5522cb6218b467a7b9f5c8dd5f81a59d199f8712b8d02a1ad6c9161647256821')
    depends_on('py-numpy@1.16.4:')
