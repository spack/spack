##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

# Original author 'Jorge Niedbalski R. <jnr@metaklass.org>'
# https://gist.github.com/niedbalski/507e974ed2d54a87ad37

import os, subprocess
import llnl.util.tty as tty
from spack.util.executable import which

class Fstab(file):
    """ This class extends file in order to implement a file reader/writer
    for file `/etc/fstab`
    """
    class Entry(object):
        """ Entry class represents a non-comment line on the `/etc/fstab` file
        """
        def __init__(self, device, mountpoint, filesystem,
                     options, d=0, p=0):
            self.device = device
            self.mountpoint = mountpoint
            self.filesystem = filesystem

            if not options:
                options = "defaults"

            self.options = options
            self.d = d
            self.p = p

        def __eq__(self, o):
            return str(self) == str(o)

        def __str__(self):
            return "{} {} {} {} {} {}".format(self.device,
                                              self.mountpoint,
                                              self.filesystem,
                                              self.options,
                                              self.d,
                                              self.p)

    DEFAULT_PATH = os.path.join(os.path.sep, 'etc', 'fstab')

    def __init__(self, path=None):
        self._check_privilege()

        if path:
            self._path = path
        else:
            self._path = self.DEFAULT_PATH
        file.__init__(self, self._path, 'r+')

    def _check_privilege(self):
        if os.geteuid() != 0:
            tty.die("To install a permanent boostrap environment root rights are required")

    def _hydrate_entry(self, line):
        return Fstab.Entry(*filter(
            lambda x: x not in ('', None),
            line.strip("\n").split(" ")))

    @property
    def entries(self):
        self.seek(0)
        for line in self.readlines():
            try:
                if not line.startswith("#"):
                    yield self._hydrate_entry(line)
            except ValueError:
                pass

    def get_entry_by_attr(self, attr, value):
        for entry in self.entries:
            e_attr = getattr(entry, attr)
            if e_attr == value:
                return entry
        return None

    def add_entry(self, entry):
        if self.get_entry_by_attr('device', entry.device):
            return False

        self.write(str(entry) + '\n')
        self.truncate()
        return entry

    def remove_entry(self, entry):
        self.seek(0)

        lines = self.readlines()

        found = False
        for index, line in enumerate(lines):
            if not line.startswith("#"):
                if self._hydrate_entry(line) == entry:
                    found = True
                    break

        if not found:
            return False

        lines.remove(line)

        self.seek(0)
        self.write(''.join(lines))
        self.truncate()
        return True

    @classmethod
    def remove_by_mountpoint(cls, mountpoint, path=None):
        fstab = cls(path=path)
        entry = fstab.get_entry_by_attr('mountpoint', mountpoint)
        if entry:
            return fstab.remove_entry(entry)
        return False

    @classmethod
    def add(cls, device, mountpoint, filesystem, options=None, path=None):
        return cls(path=path).add_entry(Fstab.Entry(device, mountpoint, \
                                                    filesystem, options))
