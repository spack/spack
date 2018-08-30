##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import os

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

from spack.util.editor import editor


def pre_install(spec):
    """This hook handles global license setup for licensed software."""
    pkg = spec.package
    if pkg.license_required and not pkg.spec.external:
        set_up_license(pkg)


def set_up_license(pkg):
    """Prompt the user, letting them know that a license is required.

    For packages that rely on license files, a global license file is
    created and opened for editing.

    For packages that rely on environment variables to point to a
    license, a warning message is printed.

    For all other packages, documentation on how to set up a license
    is printed."""

    # If the license can be stored in a file, create one
    if pkg.license_files:
        license_path = pkg.global_license_file
        if not os.path.exists(license_path):
            # Create a new license file
            write_license_file(pkg, license_path)
            # Open up file in user's favorite $EDITOR for editing
            editor(license_path)
            tty.msg("Added global license file %s" % license_path)
        else:
            # Use already existing license file
            tty.msg("Found already existing license %s" % license_path)

    # If not a file, what about an environment variable?
    elif pkg.license_vars:
        tty.warn("A license is required to use %s. Please set %s to the "
                 "full pathname to the license file, or port@host if you"
                 " store your license keys on a dedicated license server" %
                 (pkg.name, ' or '.join(pkg.license_vars)))

    # If not a file or variable, suggest a website for further info
    elif pkg.license_url:
        tty.warn("A license is required to use %s. See %s for details" %
                 (pkg.name, pkg.license_url))

    # If all else fails, you're on your own
    else:
        tty.warn("A license is required to use %s" % pkg.name)


def write_license_file(pkg, license_path):
    """Writes empty license file.

    Comments give suggestions on alternative methods of
    installing a license."""

    # License files
    linktargets = ""
    for f in pkg.license_files:
        linktargets += "\t%s\n" % f

    # Environment variables
    envvars = ""
    if pkg.license_vars:
        for varname in pkg.license_vars:
            envvars += "\t%s\n" % varname

    # Documentation
    url = ""
    if pkg.license_url:
        url += "\t%s\n" % pkg.license_url

    # Assemble. NB: pkg.license_comment will be prepended upon output.
    txt = """
 A license is required to use package '{0}'.

 * If your system is already properly configured for such a license, save this
   file UNCHANGED. The system may be configured if:

    - A license file is installed in a default location.
""".format(pkg.name)

    if envvars:
        txt += """\
    - One of the following environment variable(s) is set for you, possibly via
      a module file:

{0}
""".format(envvars)

    txt += """\
 * Otherwise, depending on the license you have, enter AT THE BEGINNING of
   this file:

   - the contents of your license file, or
   - the address(es) of your license server.

   After installation, the following symlink(s) will be added to point to
   this Spack-global file (relative to the installation prefix).

{0}
""".format(linktargets)

    if url:
        txt += """\
 * For further information on licensing, see:

{0}
""".format(url)

    txt += """\
 Recap:
 - You may not need to modify this file at all.
 - Otherwise, enter your license or server address AT THE BEGINNING.
"""
    # Global license directory may not already exist
    if not os.path.exists(os.path.dirname(license_path)):
        os.makedirs(os.path.dirname(license_path))

    # Output
    with open(license_path, 'w') as f:
        for line in txt.splitlines():
            f.write("{0}{1}\n".format(pkg.license_comment, line))
        f.close()


def post_install(spec):
    """This hook symlinks local licenses to the global license for
    licensed software.
    """
    pkg = spec.package
    if pkg.license_required and not pkg.spec.external:
        symlink_license(pkg)


def symlink_license(pkg):
    """Create local symlinks that point to the global license file."""
    target = pkg.global_license_file
    for filename in pkg.license_files:
        link_name = os.path.join(pkg.prefix, filename)
        link_name = os.path.abspath(link_name)
        license_dir = os.path.dirname(link_name)
        if not os.path.exists(license_dir):
            mkdirp(license_dir)

        # If example file already exists, overwrite it with a symlink
        if os.path.exists(link_name):
            os.remove(link_name)

        if os.path.exists(target):
            os.symlink(target, link_name)
            tty.msg("Added local symlink %s to global license file" %
                    link_name)
