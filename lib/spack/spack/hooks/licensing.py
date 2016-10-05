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
import os

import spack
import llnl.util.tty as tty
from llnl.util.filesystem import join_path, mkdirp


def pre_install(pkg):
    """This hook handles global license setup for licensed software."""
    if pkg.license_required:
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
            spack.editor(license_path)
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

    comment = pkg.license_comment

    # Global license directory may not already exist
    if not os.path.exists(os.path.dirname(license_path)):
        os.makedirs(os.path.dirname(license_path))
    license = open(license_path, 'w')

    # License files
    license.write("""\
{0} A license is required to use {1}.
{0}
{0} The recommended solution is to store your license key in this global
{0} license file. After installation, the following symlink(s) will be
{0} added to point to this file (relative to the installation prefix):
{0}
""".format(comment, pkg.name))

    for filename in pkg.license_files:
        license.write("{0}\t{1}\n".format(comment, filename))

    license.write("{0}\n".format(comment))

    # Environment variables
    if pkg.license_vars:
        license.write("""\
{0} Alternatively, use one of the following environment variable(s):
{0}
""".format(comment))

        for var in pkg.license_vars:
            license.write("{0}\t{1}\n".format(comment, var))

        license.write("""\
{0}
{0} If you choose to store your license in a non-standard location, you may
{0} set one of these variable(s) to the full pathname to the license file, or
{0} port@host if you store your license keys on a dedicated license server.
{0} You will likely want to set this variable in a module file so that it
{0} gets loaded every time someone tries to use {1}.
{0}
""".format(comment, pkg.name))

    # Documentation
    if pkg.license_url:
        license.write("""\
{0} For further information on how to acquire a license, please refer to:
{0}
{0}\t{1}
{0}
""".format(comment, pkg.license_url))

    license.write("""\
{0} You may enter your license below.

""".format(comment))

    license.close()


def post_install(pkg):
    """This hook symlinks local licenses to the global license for
    licensed software."""
    if pkg.license_required:
        symlink_license(pkg)


def symlink_license(pkg):
    """Create local symlinks that point to the global license file."""
    target = pkg.global_license_file
    for filename in pkg.license_files:
        link_name = join_path(pkg.prefix, filename)
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
