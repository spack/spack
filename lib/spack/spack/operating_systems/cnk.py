# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.architecture import OperatingSystem


class Cnk(OperatingSystem):
    """ Compute Node Kernel (CNK) is the node level operating system for
    the IBM Blue Gene series of supercomputers. The compute nodes of the
    Blue Gene family of supercomputers run CNK, a lightweight kernel that
    runs on each node and supports one application running for one user
    on that node."""

    def __init__(self):
        name = 'cnk'
        version = '1'
        super(Cnk, self).__init__(name, version)

    def __str__(self):
        return self.name
