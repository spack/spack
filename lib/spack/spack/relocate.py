##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
#  "Benedikt Hegner (CERN)"
#  "Patrick Gartung (FNAL)"

import os
import stat
import platform
import re
import spack
import spack.cmd
from spack.util.executable import which
from spack.util.executable import ProcessError
from llnl.util.filesystem import filter_file
import llnl.util.tty as tty


def get_patchelf():
    # as we may need patchelf, find out where it is
    if platform.system() == 'Darwin':
        return None
    patchelf_spec = spack.cmd.parse_specs("patchelf", concretize=True)[0]
    patchelf = spack.repo.get(patchelf_spec)
    if not patchelf.installed:
        patchelf.do_install()
    patchelf_executable = os.path.join(patchelf.prefix.bin, "patchelf")
    return patchelf_executable


def get_existing_elf_rpaths(path_name):
    """
    Return the RPATHS in given elf file as a list of strings.
    """
    if platform.system() == 'Linux':
        command = which(get_patchelf())
        output = command('--print-rpath', '%s' %
                         path_name, output=str, err=str)
        if command.returncode != 0:
            tty.warn('failed reading rpath for %s.' % path_name)
            return False
        return output.rstrip('\n').split(':')
    else:
        tty.die('relocation not supported for this platform')
    return


def get_relative_rpaths(path_name, orig_dir, orig_rpaths):
    rel_rpaths = []
    for rpath in orig_rpaths:
        if re.match(orig_dir, rpath):
            rel = os.path.relpath(rpath, start=os.path.dirname(path_name))
            rel_rpaths.append('$ORIGIN/%s' % rel)
        else:
            rel_rpaths.append(rpath)
    return rel_rpaths


def macho_get_paths(path_name):
    otool = which('otool')
    output = otool("-l", path_name, output=str, err=str)
    if otool.returncode != 0:
        tty.warn('failed reading rpath for %s.' % path_name)
        return False
    last_cmd = None
    idpath = ''
    rpaths = []
    deps = []
    for line in output.split('\n'):
        match = re.search('( *[a-zA-Z]+ )(.*)', line)
        if match:
            lhs = match.group(1).lstrip().rstrip()
            rhs = match.group(2)
            match2 = re.search('(.*) \(.*\)', rhs)
            if match2:
                rhs = match2.group(1)
            if lhs == 'cmd':
                last_cmd = rhs
            if lhs == 'path' and last_cmd == 'LC_RPATH':
                rpaths.append(rhs)
            if lhs == 'name' and last_cmd == 'LC_ID_DYLIB':
                idpath = rhs
            if lhs == 'name' and last_cmd == 'LC_LOAD_DYLIB':
                deps.append(rhs)
    return rpaths, deps, idpath


def macho_make_paths_relative(path_name, old_dir, rpaths, deps, idpath):
    id = None
    nrpaths = []
    ndeps = []
    if idpath:
        id = '@rpath/%s' % os.path.basename(idpath)
    for rpath in rpaths:
        if re.match(old_dir, rpath):
            rel = os.path.relpath(rpath, start=os.path.dirname(path_name))
            nrpaths.append('@loader_path/%s' % rel)
        else:
            nrpaths.append(rpath)
    for dep in deps:
        if re.match(old_dir, dep):
            rel = os.path.relpath(dep, start=os.path.dirname(path_name))
            ndeps.append('@loader_path/%s' % rel)
        else:
            ndeps.append(dep)
    return nrpaths, ndeps, id


def macho_replace_paths(old_dir, new_dir, rpaths, deps, idpath):
    id = None
    nrpaths = []
    ndeps = []
    if idpath:
        id = idpath.replace(old_dir, new_dir)
    for rpath in rpaths:
        nrpath = rpath.replace(old_dir, new_dir)
        nrpaths.append(nrpath)
    for dep in deps:
        ndep = dep.replace(old_dir, new_dir)
        ndeps.append(ndep)
    return nrpaths, ndeps, id


def modify_macho_object(path_name, old_dir, new_dir, relative):
    """
    Modify MachO binaries by changing rpaths,and id and dependency lib paths.
    Examines the output of otool -l for these three fields:
    LC_ID_DYLIB, LC_LOAD_DYLIB, LC_RPATH
    The old install dir in LC_ID_DYLIB is replaced with the new install dir
    using install_name_tool -id newid binary
    The old install dir in LC_LOAD_DYLIB is replaced with the new install dir
    using install_name_tool -change old new binary
    The old install dir in LC_RPATH is replaced with the new install dir using
    install_name_tool  -rpath old new binary
    """
    # avoid error message for libgcc_s
    if 'libgcc_' in path_name:
        return
    rpaths, deps, idpath = macho_get_paths(path_name)
    id = None
    nrpaths = []
    ndeps = []
    if relative:
        nrpaths, ndeps, id = macho_make_paths_relative(path_name,
                                                       old_dir, rpaths,
                                                       deps, idpath)
    else:
        nrpaths, ndeps, id = macho_replace_paths(old_dir, new_dir, rpaths,
                                                 deps, idpath)
    st = os.stat(path_name)
    # some installs create read-only binaries
    wmode = os.access(path_name, os.W_OK)
    if not wmode:
        try:
            os.chmod(path_name, st.st_mode | stat.S_IWUSR)
        except OSError as e:
            tty.warn(e)
    install_name_tool = which('install_name_tool')
    if id:
        try:
            install_name_tool('-id', id, path_name, output=str, err=str)
        except ProcessError as e:
            tty.warn(e)

    for orig, new in zip(deps, ndeps):
        try:
            install_name_tool('-change', orig, new, path_name)
        except ProcessError as e:
            tty.warn(e)

    for orig, new in zip(rpaths, nrpaths):
        try:
            install_name_tool('-rpath', orig, new, path_name)
        except ProcessError as e:
            tty.warn(e)
    try:
        os.chmod(path_name, st.st_mode)
    except OSError as e:
        tty.warn(e)
    return


def get_filetype(path_name):
    """
    Check the output of the file command for given string.
    """
    bash = which('bash')
    output = bash('-c', 'LC_ALL=C && file -b -h %s' % path_name,
                  output=str, err=str)
    if bash.returncode != 0:
        tty.warn('getting filetype of "%s" failed' % path_name)
        return None
    return output.strip()


def modify_elf_object(path_name, orig_rpath, new_rpath):
    """
    Replace RPATH's in given elf object
    """
    st = os.stat(path_name)
    wmode = os.access(path_name, os.W_OK)
    if not wmode:
        os.chmod(path_name, st.st_mode | stat.S_IWUSR)
    if platform.system() == 'Linux':
        new_joined = ':'.join(new_rpath)
        command = which(get_patchelf())
        output = command('--force-rpath', '--set-rpath', '%s' % new_joined,
                         '%s' % path_name, output=str, cmd=str)
        if command.returncode != 0:
            tty.warn('failed writing rpath for %s.' % path_name)
            tty.warn(output)
    else:
        tty.die('relocation not supported for this platform')
    os.chmod(path_name, st.st_mode)


def needs_binary_relocation(filetype):
    """
    Check whether the given filetype is a binary that may need relocation.
    """
    retval = False
    if "relocatable" in filetype:
        return False
    if platform.system() == 'Darwin':
        return ('Mach-O' in filetype)
    elif platform.system() == 'Linux':
        return ('ELF' in filetype)
    else:
        tty.die("Relocation not implemented for %s" % platform.system())
    return retval


def needs_text_relocation(filetype):
    """
    Check whether the given filetype needs relocation.
    """
    return ("text" in filetype)


def relocate_binary(path_name, old_dir, new_dir):
    """
    Change RPATHs in given elf or mach-o file
    """
    if platform.system() == 'Darwin':
        modify_macho_object(path_name, old_dir, new_dir, relative=False)
    elif platform.system() == 'Linux':
        orig_rpaths = get_existing_elf_rpaths(path_name)
        new_rpaths = substitute_rpath(orig_rpaths, old_dir, new_dir)
        modify_elf_object(path_name, orig_rpaths, new_rpaths)
    else:
        tty.die("Relocation not implemented for %s" % platform.system())


def make_binary_relative(path_name, old_dir):
    """
    Change RPATHs in given elf or mach-o file to relative
    """
    if platform.system() == 'Darwin':
        new_dir = ''
        modify_macho_object(path_name, old_dir, new_dir, relative=True)
    elif platform.system() == 'Linux':
        orig_rpaths = get_existing_elf_rpaths(path_name)
        new_rpaths = get_relative_rpaths(path_name, old_dir, orig_rpaths)
        modify_elf_object(path_name, orig_rpaths, new_rpaths)
    else:
        tty.die("Prelocation not implemented for %s" % platform.system())


def relocate_text(path_name, old_dir, new_dir):
    """
    Replace old path with new path in text files
    """
    filter_file("r'%s'" % old_dir, "r'%s'" % new_dir, path_name)


def substitute_rpath(orig_rpath, topdir, new_root_path):
    """
    Replace
    """
    new_rpaths = []
    for path in orig_rpath:
        new_rpath = path.replace(topdir, new_root_path)
        new_rpaths.append(new_rpath)
    return new_rpaths
