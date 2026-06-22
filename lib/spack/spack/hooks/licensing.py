# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.llnl.util.tty as tty
import spack.util.editor as ed
from spack.llnl.util.filesystem import mkdirp, symlink


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

            # use spack.util.executable so the editor does not hang on return here
            ed.editor(license_path, exec_fn=ed.executable)
        else:
            # Use already existing license file
            tty.msg(f"Found already existing license {license_path}")

    # If not a file, what about an environment variable?
    elif pkg.license_vars:
        tty.warn(
            "A license is required to use {}. Please set {} to the "
            "full pathname to the license file, or port@host if you"
            " store your license keys on a dedicated license server".format(
                pkg.name, " or ".join(pkg.license_vars)
            )
        )

    # If not a file or variable, suggest a website for further info
    elif pkg.license_url:
        tty.warn(f"A license is required to use {pkg.name}. See {pkg.license_url} for details")

    # If all else fails, you're on your own
    else:
        tty.warn(f"A license is required to use {pkg.name}")


def write_license_file(pkg, license_path):
    """Writes empty license file.

    Comments give suggestions on alternative methods of
    installing a license."""

    # License files
    linktargets = ""
    for f in pkg.license_files:
        linktargets += f"\t{f}\n"

    # Environment variables
    envvars = ""
    if pkg.license_vars:
        for varname in pkg.license_vars:
            envvars += f"\t{varname}\n"

    # Documentation
    url = ""
    if pkg.license_url:
        url += f"\t{pkg.license_url}\n"

    # Assemble. NB: pkg.license_comment will be prepended upon output.
    txt = f"""
 A license is required to use package '{pkg.name}'.

 * If your system is already properly configured for such a license, save this
   file UNCHANGED. The system may be configured if:

    - A license file is installed in a default location.
"""

    if envvars:
        txt += f"""\
    - One of the following environment variable(s) is set for you, possibly via
      a module file:

{envvars}
"""

    txt += f"""\
 * Otherwise, depending on the license you have, enter AT THE BEGINNING of
   this file:

   - the contents of your license file, or
   - the address(es) of your license server.

   After installation, the following symlink(s) will be added to point to
   this Spack-global file (relative to the installation prefix).

{linktargets}
"""

    if url:
        txt += f"""\
 * For further information on licensing, see:

{url}
"""

    txt += """\
 Recap:
 - You may not need to modify this file at all.
 - Otherwise, enter your license or server address AT THE BEGINNING.
"""
    # Global license directory may not already exist
    if not os.path.exists(os.path.dirname(license_path)):
        os.makedirs(os.path.dirname(license_path))

    # Output
    with open(license_path, "w", encoding="utf-8") as f:
        for line in txt.splitlines():
            f.write(f"{pkg.license_comment}{line}\n")
        f.close()


def post_install(spec, explicit=None):
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
        if os.path.lexists(link_name):
            os.remove(link_name)

        if os.path.exists(target):
            symlink(target, link_name)
            tty.msg(f"Added local symlink {link_name} to global license file")
